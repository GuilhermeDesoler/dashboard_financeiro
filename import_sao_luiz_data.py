"""
Import Script for São Luiz Calçados Sales Data
This script will help import the sales data from the CSV file into the system

Prerequisites:
1. Create a new company "São Luiz Calçados" in the Admin panel
2. Get the company_id from the created company
3. Run this script to create modalities and import sales data
"""

import csv
import re
from datetime import datetime
from decimal import Decimal
from dependencies import get_container

# Payment modalities with suggested colors
MODALITIES = [
    {"name": "Pix Sicredi", "color": "#00C853", "type": "pix"},
    {"name": "Pix Sicoob", "color": "#00E676", "type": "pix"},
    {"name": "Débito Sicredi", "color": "#2196F3", "type": "debito"},
    {"name": "Débito Sicoob", "color": "#03A9F4", "type": "debito"},
    {"name": "Crédito Av Sicredi", "color": "#FF9800", "type": "credito"},
    {"name": "Crédito Av Sicoob", "color": "#FFB74D", "type": "credito"},
    {"name": "Dinheiro", "color": "#4CAF50", "type": "dinheiro"},
    {"name": "Crediário", "color": "#9C27B0", "type": "crediario"},
    {"name": "Recebimento Crediario", "color": "#BA68C8", "type": "crediario"},
    {"name": "BonusCred", "color": "#E91E63", "type": "credito"},
    {"name": "Parcelado 2 a 4 Sicredi", "color": "#FF5722", "type": "parcelado"},
    {"name": "Parcelado 5 a 6 Sicredi", "color": "#F44336", "type": "parcelado"},
    {"name": "Parcelado 2 a 4 Sicoob", "color": "#FF6F00", "type": "parcelado"},
    {"name": "Parcelado 5 a 6 Sicoob", "color": "#FF8F00", "type": "parcelado"},
]


def parse_brazilian_currency(value_str: str) -> float:
    """
    Convert Brazilian currency format to float
    Example: "R$ 1.234,56" -> 1234.56
    """
    if not value_str or value_str.strip() == "":
        return 0.0

    # Remove "R$" and spaces
    value_str = value_str.replace("R$", "").strip()

    # Replace thousand separator (.) with nothing
    value_str = value_str.replace(".", "")

    # Replace decimal separator (,) with .
    value_str = value_str.replace(",", ".")

    try:
        return float(value_str)
    except ValueError:
        return 0.0


def parse_date(date_str: str) -> datetime:
    """
    Parse Brazilian date format DD/MM/YYYY to datetime
    """
    return datetime.strptime(date_str.strip(), "%d/%m/%Y")


def create_modalities(company_id: str, dry_run: bool = True):
    """
    Create payment modalities for São Luiz Calçados

    Args:
        company_id: The UUID of the company
        dry_run: If True, only print what would be created
    """
    print(f"\n{'=' * 60}")
    print(f"CREATING PAYMENT MODALITIES FOR COMPANY: {company_id}")
    print(f"{'=' * 60}\n")

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")

    container = get_container()
    modality_use_cases = container.modality_use_cases

    created_modalities = {}

    for modality in MODALITIES:
        if dry_run:
            print(f"Would create: {modality['name']:30} | Color: {modality['color']} | Type: {modality['type']}")
        else:
            try:
                created = modality_use_cases.create_modality(
                    company_id=company_id,
                    name=modality['name'],
                    color=modality['color']
                )
                created_modalities[modality['name']] = created.id
                print(f"✅ Created: {modality['name']:30} | ID: {created.id}")
            except Exception as e:
                print(f"❌ Error creating {modality['name']}: {str(e)}")

    return created_modalities


def import_sales_data(csv_file_path: str, company_id: str, modality_map: dict, dry_run: bool = True):
    """
    Import sales data from CSV file

    Args:
        csv_file_path: Path to the CSV file
        company_id: The UUID of the company
        modality_map: Dictionary mapping modality names to their IDs
        dry_run: If True, only print what would be imported
    """
    print(f"\n{'=' * 60}")
    print(f"IMPORTING SALES DATA")
    print(f"{'=' * 60}\n")

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")

    container = get_container()
    financial_entry_use_cases = container.financial_entry_use_cases

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse header to get dates
    header_line = lines[1].strip().split(',')
    dates = []
    date_indices = []

    for i in range(0, len(header_line), 2):
        if i < len(header_line):
            date_str = header_line[i].strip().replace('"', '')
            if '/' in date_str and date_str.count('/') == 2:
                try:
                    date_obj = parse_date(date_str)
                    dates.append(date_obj)
                    date_indices.append(i)
                except:
                    pass

    print(f"Found {len(dates)} dates in the CSV")
    print(f"Date range: {dates[0].strftime('%d/%m/%Y')} to {dates[-1].strftime('%d/%m/%Y')}\n")

    total_transactions = 0
    total_value = 0.0
    transactions_by_modality = {}

    # Process data lines (skip first 3 lines: total, header, empty)
    for line_idx in range(3, len(lines)):
        line = lines[line_idx].strip()
        if not line:
            continue

        parts = line.split(',')

        # Process each date column
        for date_idx, date_obj in enumerate(dates):
            col_idx = date_indices[date_idx]

            # Value is at col_idx, modality is at col_idx + 1
            if col_idx < len(parts) and col_idx + 1 < len(parts):
                value_str = parts[col_idx].strip().replace('"', '')
                modality_str = parts[col_idx + 1].strip().replace('"', '')

                # Clean up encoding issues
                modality_str = (modality_str
                    .replace('Ã©', 'é')
                    .replace('Ã¡', 'á')
                    .replace('Ã­', 'í'))

                # Skip if no value or modality
                if not value_str or not modality_str or modality_str == "Modalidade":
                    continue

                # Skip if value doesn't start with R$
                if not value_str.startswith('R$'):
                    continue

                value = parse_brazilian_currency(value_str)

                if value > 0:
                    # Track statistics
                    total_transactions += 1
                    total_value += value

                    if modality_str not in transactions_by_modality:
                        transactions_by_modality[modality_str] = {
                            'count': 0,
                            'total': 0.0
                        }

                    transactions_by_modality[modality_str]['count'] += 1
                    transactions_by_modality[modality_str]['total'] += value

                    if dry_run:
                        if total_transactions <= 10:  # Show first 10 only in dry run
                            modality_id = modality_map.get(modality_str, "NOT_FOUND")
                            print(f"Would import: {date_obj.strftime('%d/%m/%Y')} | {value_str:15} | {modality_str:30} | Modality ID: {modality_id}")
                    else:
                        try:
                            modality_id = modality_map.get(modality_str)
                            if not modality_id:
                                print(f"⚠️  Skipping: Unknown modality '{modality_str}'")
                                continue

                            financial_entry_use_cases.create_financial_entry(
                                company_id=company_id,
                                date=date_obj,
                                value=value,
                                description=f"Venda - {modality_str}",
                                entry_type="receita",
                                modality_id=modality_id
                            )

                            if total_transactions % 100 == 0:
                                print(f"✅ Imported {total_transactions} transactions...")

                        except Exception as e:
                            print(f"❌ Error importing transaction: {str(e)}")

    # Print summary
    print(f"\n{'=' * 60}")
    print("IMPORT SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total transactions: {total_transactions}")
    print(f"Total value: R$ {total_value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"\nTransactions by modality:")

    for modality, stats in sorted(transactions_by_modality.items(), key=lambda x: x[1]['total'], reverse=True):
        value_fmt = f"R$ {stats['total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        print(f"  {modality:35} | {stats['count']:4} vendas | {value_fmt}")

    print(f"{'=' * 60}\n")


def main():
    """
    Main function to run the import

    INSTRUCTIONS:
    1. First, create the company "São Luiz Calçados" in the Admin panel
    2. Copy the company_id from the created company
    3. Update the COMPANY_ID variable below
    4. Run with dry_run=True first to verify the data
    5. Run with dry_run=False to actually import the data
    """

    # ⚠️ UPDATE THIS WITH THE ACTUAL COMPANY ID ⚠️
    COMPANY_ID = "YOUR_COMPANY_ID_HERE"

    # Path to the CSV file
    CSV_FILE_PATH = "Cópia de Financeiro São Luiz Calçados - Vendas Dezembro_25.csv"

    # Set to False when ready to actually import
    DRY_RUN = True

    if COMPANY_ID == "YOUR_COMPANY_ID_HERE":
        print("\n⚠️  ERROR: Please update the COMPANY_ID variable in the script")
        print("1. Create the company 'São Luiz Calçados' in the Admin panel")
        print("2. Copy the company_id")
        print("3. Update COMPANY_ID in this script")
        print("4. Run the script again\n")
        return

    print(f"\n{'=' * 60}")
    print("SÃO LUIZ CALÇADOS - DATA IMPORT SCRIPT")
    print(f"{'=' * 60}\n")
    print(f"Company ID: {COMPANY_ID}")
    print(f"CSV File: {CSV_FILE_PATH}")
    print(f"Mode: {'DRY RUN (no changes)' if DRY_RUN else 'LIVE IMPORT'}")
    print(f"{'=' * 60}\n")

    # Step 1: Create modalities
    print("\n📋 STEP 1: Creating payment modalities...")
    modality_map = create_modalities(COMPANY_ID, dry_run=DRY_RUN)

    if not DRY_RUN and modality_map:
        # Step 2: Import sales data
        print("\n📊 STEP 2: Importing sales data...")
        import_sales_data(CSV_FILE_PATH, COMPANY_ID, modality_map, dry_run=DRY_RUN)
    elif DRY_RUN:
        print("\n⚠️  Skipping sales import in DRY RUN mode")
        print("Set DRY_RUN = False to actually import the data")

    print("\n✅ Script completed!")


if __name__ == "__main__":
    main()
