import json

# Database configuration
DB_CONFIG = {
    'db_name': 'holdings.db',  # Only db_name is needed for SQLite
    'sql_file_name': 'holdings.sql'
}

with open('./data/mutual_funds_data.json') as f:
    json_data = json.load(f)

# Convert JSON to SQL
def json_to_sql(json_data, db_config=DB_CONFIG):
    print(f'Converting JSON data to SQL for {json_data[0]["name"]}...')
    try:
        # Create SQL file
        with open(db_config['sql_file_name'], 'w') as f:
            # Create table for holdings
            f.write(''' 
                CREATE TABLE IF NOT EXISTS holdings (
                    fund_name TEXT,
                    company_name TEXT,
                    data JSON
                );
            ''')

            # Insert data into table
            for fund in json_data:
                fund_name = fund.get('name', 'Unknown Fund')  # Default to 'Unknown Fund' if name is missing
            
                for holding in fund.get('holdings', []):
                    company_name = holding.get('name', 'Unknown Company')  # Default to 'Unknown Company' if name is missing
                    data_values = json.dumps(holding.get('data', []))  # Use json.dumps to convert the list to a JSON string
                    f.write('''
                        INSERT INTO holdings (fund_name, company_name, data)
                        VALUES ('{}', '{}', '{}');
                    '''.format(fund_name, company_name, data_values))

    except Exception as e:
        print(f"Error: {e}")


# Call the function to convert JSON to SQL
json_to_sql(json_data, DB_CONFIG)

