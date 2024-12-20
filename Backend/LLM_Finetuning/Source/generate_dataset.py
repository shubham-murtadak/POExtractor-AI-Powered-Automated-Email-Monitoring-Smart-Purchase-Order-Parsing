import pandas as pd
from sklearn.model_selection import train_test_split

# Load the Excel file
file_path = '.\Data\sythetic_data.xlsx'
df = pd.read_excel(file_path)

# Combine 'subject' and 'body' into a single 'email' column
df['email'] = df['Subject'] + " " + df['Body']

# Extract 'response' from 'llm response' column (we assume 'llm response' is already in the correct format)
df['response'] = df['LLM Response'].apply(lambda x: x)  # If the 'llm response' is already in dictionary format, adjust this as needed

# Select only the 'email' and 'response' columns
df = df[['email', 'response']]

# Split the dataset into train and test sets (80% train, 20% test)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Save train and test DataFrames as CSV
train_df.to_csv('.\\Data\\Split_data\\train.csv', index=False)
test_df.to_csv('.\\Data\\Split_data\\test.csv', index=False)

# Show the datasets' info
print("Training dataset shape:", train_df.shape)
print("Testing dataset shape:", test_df.shape)
