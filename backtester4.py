# test the script
# import libraries
import pandas as pd
import os
from datetime import datetime

# function to log trades
def log_trade_to_csv(trade_data):
    file_path = "trade_log.csv"
    columns = ['Timestamp', 'Stock', 'Action', 'Price', 'User']
    trade_df = pd.DataFrame(trade_data, columns=columns)

    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path)
        trade_df = pd.concat([old_df, trade_df], ignore_index=True)

    trade_df.to_csv(file_path, index=False)

# backtest strategy
def backtest_strategy(df, stock_name):
    capital = 100000  # per stock
    portfolio = 0
    position = 0
    buy_price = 0
    trade_log = []

    df = df.copy()
    df['Action'] = None
    df['Portfolio Value'] = float(capital)

    for i in range(len(df) - 1):
        row = df.iloc[i]
        next_row = df.iloc[i + 1]  # action happens at next day's close
        date, signal, close = row['Date'], row['Signal'], row['Close']

        # buy
        if signal == 'Buy' and position == 0:
            buy_price = next_row['Close']
            position = capital / buy_price
            capital -= position * buy_price
            portfolio = position * buy_price
            df.at[i + 1, 'Action'] = f"BUY @ ₹{buy_price:.2f}"
            trade_log.append((
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                stock_name,
                'Buy',
                round(buy_price, 2),
                'Backtest'
            ))

        # sell
        elif signal == 'Sell' and position > 0:
            sell_price = next_row['Close']
            capital += position * sell_price
            position = 0
            portfolio = 0
            df.at[i + 1, 'Action'] = f"SELL @ ₹{sell_price:.2f}"
            trade_log.append((
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                stock_name,
                'Sell',
                round(sell_price, 2),
                'Backtest'
            ))

        # update portfolio value
        if position > 0:
            df.at[i + 1, 'Portfolio Value'] = float(position * next_row['Close'])
        else:
            df.at[i + 1, 'Portfolio Value'] = capital + portfolio

    final_value = float(capital) if position == 0 else float(position * df.iloc[-1]['Close'])
    return df, final_value, trade_log

# run backtest
def run_backtest():
    folder = "stock_data"
    stocks = ['TCS', 'INFY', 'HDFCBANK', 'RELIANCE', 'BHARTIARTL', 'ICICIBANK']
    total_value = 0
    all_trades = []

    for stock in stocks:
        file_path = os.path.join(folder, f"{stock}_signals.csv")
        if not os.path.exists(file_path):
            print(f"❌ Missing: {file_path}")
            continue

        # read the file
        df = pd.read_csv(file_path)
        df_bt, final_value, trades = backtest_strategy(df, stock)
        total_value += final_value

        # save the backtested file
        output_path = os.path.join(folder, f"{stock}_backtest.csv")
        df_bt.to_csv(output_path, index=False)

        print(f"✅ Backtest complete for {stock}: Final value ₹{float(final_value):,.2f}")
        print(f"📊 Trades: {trades}")
        all_trades.extend(trades)

    # save all trades to trade_log.csv
    if all_trades:
        log_trade_to_csv(all_trades)

    print(f"\n💼 Final portfolio value: ₹{total_value:,.2f}")
    print(f"📈 Net P&L: ₹{total_value - 600000:,.2f}")

if __name__ == "__main__":
    run_backtest()
