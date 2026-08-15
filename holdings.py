import requests, json, datetime, os
WALLET_ADDRESS = "TC4ugDg9KE1KGDZ5Su7aaKh8FujeYj486Z"
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
def get_trc20_balance():
    url = f"https://api.trongrid.io/v1/accounts/{WALLET_ADDRESS}"
    r = requests.get(url, headers={"Accept": "application/json"}).json()
    if 'data' not in r or not r['data']:
        return 0
    tokens = r['data'][0].get('trc20', [])
    for t in tokens:
        for contract, val in t.items():
            if contract == USDT_CONTRACT:
                return int(val) / 1000000
    return 0
balance = get_trc20_balance()
print(f"Balance: {balance} USDT")
history_file = "history.json"
history = []
if os.path.exists(history_file):
    try:
        with open(history_file) as f:
            history = json.load(f)
    except:
        pass
history.append({"date": datetime.datetime.utcnow().isoformat(), "balance": balance})
with open(history_file, "w") as f:
    json.dump(history, f, indent=2)
with open("README.md", "w") as f:
    f.write(f"# My TRC20 USDT Portfolio\n\nLast Updated: {datetime.datetime.utcnow()}\n\n## Balance: {balance:.2f} USDT\nWallet: TC4ugD...j486Z\n")
