
import pandas as pd

users = [f'User_{i+1}' for i in range(10)]
folders = [f'Folder_{i+1}' for i in range(21)]

data = []
for user in users:
    for folder in folders:
        data.append({'User Name': user, 'Folder Name': folder})

df = pd.DataFrame(data)

permission_types = ['Read Access', 'Write Access', 'Modify Access', 'Delete Access', 'Full Control']
for perm in permission_types:
    df[perm] = False  # Initialize with False for checkboxes

df.to_excel('Permissions_Matrix.xlsx', index=False)

print('Permissions_Matrix.xlsx created successfully.')


