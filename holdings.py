import requests, json, datetime, os

WALLET_ADDRESS = "TC4ugDg9KE1KGDZ5Su7aaKh8FujeYj486Z"
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

def get_balances():
    url = f"https://api.trongrid.io/v1/accounts/{WALLET_ADDRESS}"
    r = requests.get(url, headers={"Accept": "application/json"}).json()
    if 'data' not in r or not r['data']:
        return 0, 0
    data = r['data'][0]
    trx_balance = data.get('balance', 0) / 1000000 # TRX is in sun
    usdt_balance = 0
    tokens = data.get('trc20', [])
    for t in tokens:
        for contract, val in t.items():
            if contract == USDT_CONTRACT:
                usdt_balance = int(val) / 1000000
    return trx_balance, usdt_balance

trx, usdt = get_balances()
print(f"TRX Balance: {trx} TRX")
print(f"USDT Balance: {usdt} USDT")

with open("README.md", "w") as f:
    f.write(f"# My TRON Portfolio\n\n")
    f.write(f"Last Updated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n")
    f.write(f"## Balances for TC4ugD...j486Z\n\n")
    f.write(f"- **TRX:** {trx:.4f} TRX\n")
    f.write(f"- **USDT (TRC20):** {usdt:.2f} USDT\n\n")
    f.write(f"Total TRX Value: ~${trx*0.15:.2f} est.\n")
    f.write(f"[View on Tronscan](https://tronscan.org/#/address/{WALLET_ADDRESS})\n")

history_file = "history.json"
history = []
if os.path.exists(history_file):
    try:
        with open(history_file) as f:
            history = json.load(f)
    except:
        pass
history.append({"date": datetime.datetime.utcnow().isoformat(), "trx": trx, "usdt": usdt})
with open(history_file, "w") as f:
    json.dump(history[-500:], f, indent=2)
