"""
Script para executar o import e capturar apenas os erros
"""
import subprocess
import sys

print("Executando import e capturando output...")

# Executa o comando e captura a saída
process = subprocess.Popen(
    ['python3', 'import_lancamentos_v2.py', 'execute'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Envia "sim" para confirmar
stdout, _ = process.communicate(input="sim\n")

# Salva o log completo
with open("import_full_log.txt", "w", encoding="utf-8") as f:
    f.write(stdout)

print(f"\n✅ Log completo salvo em: import_full_log.txt")

# Procura por erros
erros = []
linhas = stdout.split('\n')
for i, linha in enumerate(linhas):
    if '❌ ERRO' in linha or '❌ EXCEÇÃO' in linha:
        # Captura 5 linhas após o erro
        erro_completo = '\n'.join(linhas[i:i+6])
        erros.append(erro_completo)

if erros:
    print(f"\n🔍 Encontrados {len(erros)} erro(s):\n")
    for i, erro in enumerate(erros, 1):
        print(f"--- Erro {i} ---")
        print(erro)
        print()
else:
    print("\n✅ Nenhum erro encontrado!")

# Mostra o resumo
for linha in linhas:
    if 'RESUMO:' in linha:
        idx = linhas.index(linha)
        print('\n'.join(linhas[idx:idx+8]))
        break
