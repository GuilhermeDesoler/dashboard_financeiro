import streamlit as st
import requests
from config import Environment


def render_api_health_check():
    """Renderiza um componente de verificação de saúde da API"""

    env = Environment()
    base_url = env.base_url.rstrip("/")

    with st.expander("🔍 Debug da API", expanded=False):
        st.markdown("### Informações de Conexão")
        st.code(f"Base URL: {base_url}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Testar Conexão", use_container_width=True):
                try:
                    response = requests.get(f"{base_url}/health", timeout=10)
                    if response.status_code == 200:
                        st.success("✅ API está respondendo!")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Status Code: {response.status_code}")
                        st.text(response.text[:500])
                except Exception as e:
                    st.error(f"❌ Erro ao conectar: {str(e)}")

        with col2:
            if st.button("📋 Testar Endpoints", use_container_width=True):
                endpoints_to_test = [
                    "/api/payment-modalities",
                    "/api/financial-entries",
                ]

                for endpoint in endpoints_to_test:
                    try:
                        url = f"{base_url}{endpoint}"
                        response = requests.get(url, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            st.success(f"✅ {endpoint} - {len(data)} itens")
                        else:
                            st.warning(f"⚠️ {endpoint} - Status: {response.status_code}")
                    except Exception as e:
                        st.error(f"❌ {endpoint} - Erro: {str(e)}")

        st.markdown("---")
        st.markdown("### Teste Manual de Filtro de Datas")

        test_start = st.text_input("Start Date", value="2025-12-01")
        test_end = st.text_input("End Date", value="2025-12-31")

        if st.button("🧪 Testar Filtro", use_container_width=True):
            try:
                url = f"{base_url}/api/financial-entries"
                params = {"start_date": test_start, "end_date": test_end}

                st.info(f"Request: GET {url}")
                st.json({"params": params})

                response = requests.get(url, params=params, timeout=10)

                st.info(f"Response Status: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Sucesso! {len(data)} lançamentos encontrados")
                    st.json(data)
                else:
                    st.error(f"❌ Erro {response.status_code}")
                    st.text(response.text[:1000])

            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
