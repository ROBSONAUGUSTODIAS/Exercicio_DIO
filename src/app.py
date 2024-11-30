import streamlit as st
from datetime import datetime

# Lista de BINs válidos para teste (apenas exemplos, normalmente se usa uma API ou banco de dados)
VALID_BINS = ["4539", "6011", "5500", "4000", "3400", "3000"]

def validate_card_number(card_number):
    """Função para validar o número do cartão usando o Algoritmo de Luhn."""
    card_number = card_number.replace(" ", "")  # Remover espaços
    if not card_number.isdigit():
        return False

    # Algoritmo de Luhn
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def validate_bin(card_number):
    """Função para validar se o BIN (primeiros 6 dígitos) é válido."""
    bin_number = card_number.replace(" ", "")[:4]  # Considera os 4 primeiros dígitos (para simplificação)
    return bin_number in VALID_BINS

def validate_expiration_date(expiration_date):
    """Função para validar a data de validade do cartão."""
    try:
        expiration = datetime.strptime(expiration_date, "%m/%Y")
        if expiration < datetime.now():
            return False
        return True
    except ValueError:
        return False

def detect_fraud(card_number, name, expiration_date):
    """Função simples para detectar possíveis fraudes."""
    card_number = card_number.replace(" ", "")

    # Verificar se o BIN é inválido
    if not validate_bin(card_number):
        return "O BIN do cartão não é válido. Isso pode indicar uma fraude."

    # Verificar se o nome é muito curto ou contém caracteres inválidos
    if len(name.split()) < 2 or not name.replace(" ", "").isalpha():
        return "O nome fornecido parece inválido. Isso pode indicar uma fraude."

    # Verificar se a validade está em um formato anormal (exemplo: antes de 2000)
    try:
        expiration = datetime.strptime(expiration_date, "%m/%Y")
        if expiration.year < 2000:
            return "A data de validade do cartão é anormal. Isso pode indicar uma fraude."
    except ValueError:
        return "A data de validade fornecida está incorreta."

    # Caso nenhuma regra indique fraude
    return None

def configure_interface():
    st.title("Validação de Cartão com Detecção de Fraude")

    # Entrada do nome no cartão
    name = st.text_input("Nome no Cartão")
    
    # Entrada do número do cartão
    card_number = st.text_input("Número do Cartão (16 dígitos)")
    
    # Entrada da validade do cartão
    expiration_date = st.text_input("Data de Validade (MM/AAAA)")
    
    # Upload da imagem do cartão
    uploaded_file = st.file_uploader("Faça upload da imagem do cartão", type=["png", "jpg", "jpeg"])

    # Exibir a imagem carregada (se houver)
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Imagem do Cartão", use_column_width=True)
        st.success("Imagem carregada com sucesso!")

    # Botão de validação
    if st.button("Validar e Detectar Fraude"):
        # Verificar se os campos foram preenchidos corretamente
        if not name:
            st.error("Por favor, insira o nome no cartão.")
        elif not card_number or not validate_card_number(card_number):
            st.error("Número do cartão inválido. Verifique e tente novamente.")
        elif not expiration_date or not validate_expiration_date(expiration_date):
            st.error("Data de validade inválida ou expirada. Verifique e tente novamente.")
        elif uploaded_file is None:
            st.error("Por favor, faça o upload da imagem do cartão.")
        else:
            # Verificar fraude
            fraud_message = detect_fraud(card_number, name, expiration_date)
            if fraud_message:
                st.error(f"⚠️ Atenção: {fraud_message}")
            else:
                st.success(f"Cartão válido e sem indícios de fraude! Nome: {name}, Número: {card_number}, Validade: {expiration_date}")

if __name__ == "__main__":
    configure_interface()
