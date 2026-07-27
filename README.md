# Portfolio Value Tracker
#### Video Demo: <URL HERE>
#### Description:

##### What it does
This is a portfolio tracker that calculates both the value and return of an investment portfolio over time. When investing across multiple brokerages, it can be difficult to get a single, combined view of how your overall portfolio is actually performing. This program addresses that by letting the user enter any number of holdings, including a ticker symbol, number of shares purchased, and purchase date. It then uses live data from Yahoo Finance, via the `yfinance` library, to produce a graph of portfolio value over time along with the total percentage return.

##### Usage
When the user runs this program, they are first prompted for a "Ticker Symbol", which must exactly match a valid symbol recognised by Yahoo finance. They are then asked for the "Quantity of Holdings", which must be an integer, and "Date of Purchase", entered in YYYY-MM-DD format. These three inputs are the minimum requirement to add a single holding. The user is then asked "Add another holding? (y/n)" and can enter y or n, case-insensitively, to add further holdings or finish. Once all holdings have been entered, typing n exits the input loop. The program then prints the total portfolio return in the terminal and saves a graph of portfolio value over time, generated using `matplotlib`, covering the period from the earliest purchase date to the current date.

#### How it Works
`add_holdings` appends a new holding to a CSV file, given a `filepath`, a ticker, quantity, and purchase date. If the file does not already exist, it first writes a header row (`ticker`, `quantity`, `purchase_date`) before adding the new entry, so the file is created correctly on first use and simply appended to on every run afterward.

`read_holdings` reads all holdings from a CSV file, given a `filepath`, and returns them as a list of dictionaries, where each dictionary represents one holding with `ticker`, `quantity`, and `purchase_date` keys. Unlike `add_holdings`, which writes a single new entry each time it is called, `read_holdings` loops through every row in the file, building up a complete list of every holding ever recorded, so it is called at the start of each run to reconstruct the full portfolio from every previous use of the program.



