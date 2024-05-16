with open('NCUE_accounts.txt', 'r') as f:
    account = f.read().strip()
    password = f.read().strip()

print(account,password)