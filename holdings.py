import requests
import json
import os
from datetime import datetime

# --- CONFIG ---
WALLET_ADDRESS = "TC4ugDg9KE1KGDZ5Su7aaKh8FujeYj486Z"
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

README_PATH = "README.md"
HISTORY_PATH = "history.json"

def get_trc20_balance():
    url = f"https://api.trongrid.io/v1/accounts/{WALLET_ADDRESS}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if not data.get('data'):
            return 0.0, 0.0
        account_data = data['data'][0]
        trx_balance = account_data.get('balance', 0) / 1_000_000
        usdt_balance = 0.0
        for token_list in account_data.get('trc20', []):
            if isinstance(token_list, dict) and USDT_CONTRACT in token_list:
                usdt_balance = int(token_list[USDT_CONTRACT]) / 1_000_000
                break
        # fallback dict format
        if usdt_balance == 0:
            trc20_dict = account_data.get('trc20', {})
            if isinstance(trc20_dict, dict) and USDT_CONTRACT in trc20_dict:
                usdt_balance = int(trc20_dict[USDT_CONTRACT]) / 1_000_000
        return round(trx_balance, 4), round(usdt_balance, 2)
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def update_files(trx, usdt):
    now = datetime.utcnow()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S UTC")
    iso_str = now.isoformat()
    readme_content = f"""# My TRON Portfolio

Last Updated: {now_str}

## Balances for {WALLET_ADDRESS[:6]}...{WALLET_ADDRESS[-5:]}

- TRX: {trx} TRX
- USDT (TRC20): {usdt} USDT

Total TRX Value: ~${trx * 0.15:.2f} est. [View on Tronscan](https://tronscan.org/#/address/{WALLET_ADDRESS})
"""
    with open(README_PATH, 'w') as f:
        f.write(readme_content)

    history = []
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, 'r') as f:
                history = json.load(f)
        except:
            history = []
    if not history or history[-1].get('balance')!= usdt:
        history.append({"date": iso_str, "balance": usdt, "trx_balance": trx})
        history = history[-100:]
        with open(HISTORY_PATH, 'w') as f:
            json.dump(history, f, indent=2)

if __name__ == "__main__":
    trx, usdt = get_trc20_balance()
    if trx is not None:
        print(f"{WALLET_ADDRESS} | {usdt} USDT | {trx} TRX")
        update_files(trx, usdt)
