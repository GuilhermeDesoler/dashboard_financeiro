"""
Script Completo de Importação - São Luiz Calçados
Este script cria a empresa, modalidades e importa todas as transações
"""

import sys
from datetime import datetime
from dependencies import get_container

# Modalidades com cores
MODALITIES = [
    {"name": "Pix Sicredi", "color": "#00C853"},
    {"name": "Pix Sicoob", "color": "#00E676"},
    {"name": "Débito Sicredi", "color": "#2196F3"},
    {"name": "Débito Sicoob", "color": "#03A9F4"},
    {"name": "Crédito Av Sicredi", "color": "#FF9800"},
    {"name": "Crédito Av Sicoob", "color": "#FFB74D"},
    {"name": "Dinheiro", "color": "#4CAF50"},
    {"name": "Crediário", "color": "#9C27B0"},
    {"name": "Recebimento Crediario", "color": "#BA68C8"},
    {"name": "BonusCred", "color": "#E91E63"},
    {"name": "Parcelado 2 a 4 Sicredi", "color": "#FF5722"},
    {"name": "Parcelado 5 a 6 Sicredi", "color": "#F44336"},
    {"name": "Parcelado 2 a 4 Sicoob", "color": "#FF6F00"},
    {"name": "Parcelado 5 a 6 Sicoob", "color": "#FF8F00"},
]


def parse_brazilian_currency(value_str: str) -> float:
    """Convert R$ 1.234,56 to 1234.56"""
    if not value_str or not value_str.strip():
        return 0.0
    value_str = value_str.replace("R$", "").strip().replace(".", "").replace(",", ".")
    try:
        return float(value_str)
    except:
        return 0.0


def parse_date(date_str: str) -> datetime:
    """Parse DD/MM/YYYY to datetime"""
    return datetime.strptime(date_str.strip(), "%d/%m/%Y")


def main():
    print("=" * 80)
    print("IMPORTAÇÃO COMPLETA - SÃO LUIZ CALÇADOS")
    print("=" * 80)
    print()

    container = get_container()
    admin_use_cases = container.admin_use_cases
    modality_use_cases = container.payment_modality_use_cases
    financial_entry_use_cases = container.financial_entry_use_cases

    # STEP 1: Criar a empresa
    print("📋 PASSO 1: Criando empresa 'São Luiz Calçados'...")
    try:
        company = admin_use_cases.create_company(
            name="São Luiz Calçados",
            cnpj=None,
            phone=None,
            plan="basic"
        )
        company_id = company.id
        print(f"✅ Empresa criada com sucesso!")
        print(f"   ID: {company_id}")
        print(f"   Nome: {company.name}")
        print()
    except Exception as e:
        print(f"❌ Erro ao criar empresa: {str(e)}")
        print("   Verifique se a empresa já existe.")
        return

    # STEP 2: Criar modalidades
    print("💳 PASSO 2: Criando modalidades de pagamento...")
    modality_map = {}

    for idx, mod in enumerate(MODALITIES, 1):
        try:
            created = modality_use_cases.create_modality(
                name=mod['name'],
                color=mod['color']
            )
            modality_map[mod['name']] = created.id
            print(f"   {idx:2}. ✅ {mod['name']:30} | {mod['color']}")
        except Exception as e:
            print(f"   {idx:2}. ❌ {mod['name']:30} | Erro: {str(e)}")

    print(f"\n   Total: {len(modality_map)}/{len(MODALITIES)} modalidades criadas")
    print()

    # STEP 3: Importar transações do CSV
    print("📊 PASSO 3: Importando transações do CSV...")
    print()

    # Ler o arquivo CSV fornecido no documento
    csv_file = "Cópia de Financeiro São Luiz Calçados - Vendas Dezembro_25.csv"

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {csv_file}")
        print("   Por favor, coloque o arquivo CSV no diretório atual.")
        return

    # Parse header para pegar as datas
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

    print(f"   📅 Encontradas {len(dates)} datas no CSV")
    print(f"   📅 Período: {dates[0].strftime('%d/%m/%Y')} a {dates[-1].strftime('%d/%m/%Y')}")
    print()

    total_transactions = 0
    total_value = 0.0
    skipped = 0
    errors = 0

    # Processar dados (pular primeiras 3 linhas: total, header, vazio)
    for line_idx in range(3, len(lines)):
        line = lines[line_idx].strip()
        if not line:
            continue

        parts = line.split(',')

        # Processar cada coluna de data
        for date_idx, date_obj in enumerate(dates):
            col_idx = date_indices[date_idx]

            if col_idx < len(parts) and col_idx + 1 < len(parts):
                value_str = parts[col_idx].strip().replace('"', '')
                modality_str = parts[col_idx + 1].strip().replace('"', '')

                # Limpar encoding
                modality_str = (modality_str
                    .replace('Ã©', 'é')
                    .replace('Ã¡', 'á')
                    .replace('Ã­', 'í'))

                # Pular se não tem valor ou modalidade
                if not value_str or not modality_str or modality_str == "Modalidade":
                    continue

                # Pular se não começa com R$
                if not value_str.startswith('R$'):
                    continue

                value = parse_brazilian_currency(value_str)

                if value > 0:
                    modality_id = modality_map.get(modality_str)

                    if not modality_id:
                        skipped += 1
                        continue

                    try:
                        financial_entry_use_cases.create_financial_entry(
                            company_id=company_id,
                            date=date_obj,
                            value=value,
                            description=f"Venda - {modality_str}",
                            entry_type="receita",
                            modality_id=modality_id
                        )

                        total_transactions += 1
                        total_value += value

                        # Mostrar progresso a cada 50 transações
                        if total_transactions % 50 == 0:
                            print(f"   ⏳ Importadas {total_transactions} transações...")

                    except Exception as e:
                        errors += 1
                        if errors <= 5:  # Mostrar apenas os primeiros 5 erros
                            print(f"   ⚠️  Erro: {str(e)}")

    # Resumo final
    print()
    print("=" * 80)
    print("✅ IMPORTAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print()
    print(f"📊 RESUMO:")
    print(f"   Empresa: {company.name} (ID: {company_id})")
    print(f"   Modalidades criadas: {len(modality_map)}")
    print(f"   Transações importadas: {total_transactions}")
    print(f"   Valor total: R$ {total_value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"   Transações puladas: {skipped}")
    print(f"   Erros: {errors}")
    print()

    if skipped > 0:
        print(f"⚠️  {skipped} transações foram puladas (modalidade não encontrada)")
        print()

    print("=" * 80)
    print("PRÓXIMOS PASSOS:")
    print("=" * 80)
    print()
    print("1. Faça login como Super Admin")
    print("2. Use 'Impersonar' para acessar 'São Luiz Calçados'")
    print("3. Verifique o Dashboard para dezembro de 2025")
    print("4. Confirme que o total de vendas está correto")
    print()
    print(f"💡 Company ID para referência: {company_id}")
    print()


if __name__ == "__main__":
    main()
