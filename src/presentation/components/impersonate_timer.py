import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta


def render_impersonate_timer():
    if "impersonate_start_time" not in st.session_state:
        return

    total_duration = timedelta(hours=1)
    start_time = st.session_state.impersonate_start_time
    elapsed = datetime.now() - start_time
    remaining = total_duration - elapsed
    company_name = st.session_state.get('impersonating_company', 'Empresa')

    if remaining.total_seconds() <= 0:
        st.error("⏰ **Sessão de Impersonate Expirada**")
        st.warning("O tempo de 1 hora expirou. Clique no botão abaixo para voltar ao painel admin.")

        if st.button("🔙 Voltar ao Admin", type="primary", use_container_width=True, key="timer_exit"):
            from dependencies import get_container
            container = get_container()
            http_client = container.http_client

            if "impersonate_token" in st.session_state:
                del st.session_state.impersonate_token
            if "impersonating_company" in st.session_state:
                del st.session_state.impersonating_company
            if "impersonate_start_time" in st.session_state:
                del st.session_state.impersonate_start_time

            http_client.set_auth_token(st.session_state.access_token)

            st.session_state.current_page = "Admin"
            st.rerun()
        st.stop()

    remaining_seconds = int(remaining.total_seconds())

    timer_html = f"""
    <div id="timer-container">
        <style>
            :root {{
                --primary-color: #9333EA;
                --primary-light: rgba(147, 51, 234, 0.1);
            }}

            .impersonate-card {{
                background: var(--primary-light);
                border-left: 4px solid var(--primary-color);
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
            }}

            .impersonate-header {{
                font-size: 11px;
                font-weight: 600;
                color: #666;
                margin-bottom: 8px;
                letter-spacing: 0.5px;
            }}

            .company-name {{
                font-size: 16px;
                font-weight: 700;
                color: var(--primary-color);
                margin-bottom: 12px;
            }}

            .timer-display {{
                font-size: 24px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                letter-spacing: 2px;
                margin-bottom: 8px;
            }}

            .timer-label {{
                font-size: 10px;
                color: #888;
                margin-bottom: 10px;
            }}

            .progress-bar {{
                width: 100%;
                height: 6px;
                background-color: #e0e0e0;
                border-radius: 3px;
                overflow: hidden;
            }}

            .progress-fill {{
                height: 100%;
                transition: width 1s linear, background-color 0.3s ease;
                border-radius: 3px;
            }}
        </style>

        <div id="impersonate-card" class="impersonate-card">
            <div class="impersonate-header">🎭 IMPERSONANDO</div>
            <div class="company-name">{company_name}</div>
            <div class="timer-display" id="time-display">00:00:00</div>
            <div class="timer-label" id="timer-label">Tempo restante da sessão</div>
            <div class="progress-bar">
                <div class="progress-fill" id="progress"></div>
            </div>
        </div>

        <script>
            let remainingSeconds = {remaining_seconds};
            const totalSeconds = 3600; // 1 hour

            function updateTimer() {{
                if (remainingSeconds <= 0) {{
                    window.location.reload();
                    return;
                }}

                const hours = Math.floor(remainingSeconds / 3600);
                const minutes = Math.floor((remainingSeconds % 3600) / 60);
                const seconds = remainingSeconds % 60;

                const timeStr =
                    String(hours).padStart(2, '0') + ':' +
                    String(minutes).padStart(2, '0') + ':' +
                    String(seconds).padStart(2, '0');

                document.getElementById('time-display').textContent = timeStr;

                const progress = (totalSeconds - remainingSeconds) / totalSeconds;
                document.getElementById('progress').style.width = (progress * 100) + '%';

                let color;
                if (remainingSeconds < 300) {{
                    color = '#ff4444';
                    document.getElementById('timer-label').innerHTML = '🚨 ATENÇÃO: Menos de 5 minutos restantes!';
                }} else if (remainingSeconds < 600) {{
                    color = '#ff9800';
                    document.getElementById('timer-label').innerHTML = '⚠️ Tempo restante da sessão';
                }} else {{
                    color = '#4CAF50';
                    document.getElementById('timer-label').innerHTML = 'Tempo restante da sessão';
                }}

                document.getElementById('time-display').style.color = color;
                document.getElementById('progress').style.backgroundColor = color;

                remainingSeconds--;
                setTimeout(updateTimer, 1000);
            }}

            updateTimer();
        </script>
    </div>
    """
    components.html(timer_html, height=180)
