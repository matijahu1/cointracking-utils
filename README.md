# cointracking-utils

This project provides utility tools to complement [CoinTracking](https://cointracking.info). It is designed to help advanced users manage large datasets and troubleshoot balance inconsistencies effectively.

## 🚀 Why use these tools?
When dealing with high-frequency trading, margin positions, or automated bots, the volume of data can become overwhelming. These utilities help you maintain a clean and performant account by streamlining your transaction history and providing deep insights into your asset flow.

---

## 🛠 Features

### 1. Aggregation Tool 
The **Aggregation Tool** condenses high-frequency transactions of a single day into concise summary entries.
* **Performance Optimization:** Keep your account fast and organized by reducing the total number of line items.
* **Clean Records:** Consolidate hundreds of small bot trades into daily summaries without losing daily accuracy.
* **Ideal for:** High-frequency margin trading and automated trading systems.

### 2. Calculation Tool 
The **Calculation Tool** acts as a diagnostic balance tracker to help you maintain a healthy portfolio.
* **Resolve Warnings:** Specifically designed to trace "negative balance" warnings by showing the exact historical flow of a specific coin.
* **Audit Trail:** Provides a clear view of how your balances evolved based on your CSV export, making it easier to find missing deposit/withdrawal data.
* **Future Updates:** Planned features include advanced Profit & Loss (P&L) analysis.

---

## 📋 Prerequisites
Both tools process data exported from CoinTracking:
1. Log in to your CoinTracking account.
2. Export data using the format **"CSV (Full Export)"**.

---

## 🧠 Business Logic & Rules
To ensure data integrity, this tool follows specific rules for aggregating transactions (e.g. timestamp alignment).

To avoid documentation drift, the rules are documented directly within the source code:

* **Aggregation Rules:** See documentation in [`aggregator.py`](aggregation_tool/aggregator.py)

This ensures that the documentation always matches the current implementation.

---

## ⚙️ Setup & Installation

### Project Structure
The utilities are organized into two main modules:
* `aggregation_tool/`
* `calculation_tool/`

### Configuration
1. **Prepare Data Folders:** Create a `/data` subfolder inside the tool directory you wish to use.
2. **Config Setup:** Copy `/examples/config_example.json` into your new `/data` folder and rename it to `config.json`.
3. **Filter by Year:** In `config.json`, set your desired year or leave it empty (`""`) to process all available data.
4. **Reference CSV:** Enter the exact name of your exported CoinTracking CSV file in the `config.json`.

---

## 🚀 Execution

**Run** the tools from the project root using:

To run the **Aggregation Tool**:
python -m aggregation_tool.aggregation_main

To run the **Calculation Tool**:
python -m calculation_tool.calc_main

---

## 🧪 Testing

### Test Data Setup
For unit tests, anonymized CoinTracking CSV files are provided in the
`/examples` directory.

To run the unit tests successfully:

1. Create a `/data` subfolder inside the tool directory you want to test
   (e.g. `aggregation_tool/data/`).
2. Copy the required CSV test files from `/examples` into the `/data` folder.
3. Ensure that the filenames match the references defined in the unit tests.

The `/data` directory is intentionally excluded from version control
and must be created locally.

---

## ⚖️ Disclaimer
This tool is designed to work with data exported from CoinTracking. Please note that CoinTracking is not affiliated with, and has not participated in, the development of this tool.

The developers of this tool assume no responsibility or liability for any outcomes, errors, or damages that may result from its use. Use this tool entirely at your own risk, and be aware that incorrect usage may lead to data inconsistencies or errors. No warranty or guarantee is provided, and all liability is expressly disclaimed.

This is a personal tool. Issues may be answered on a best-effort basis.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.