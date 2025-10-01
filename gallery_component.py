# gallery_component.py
import streamlit.components.v1 as components

def create_gallery(image_urls, key_prefix):
    """
    Gera o código HTML/CSS/JS para uma grelha de imagens clicáveis com um modal/popup.
    """
    
    # --- CSS Styles ---
    # Estilos para a grelha, o modal, o botão de fechar, etc.
    css_styles = """
    <style>
        .gallery-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
        }
        .gallery-img {
            width: 100%;
            height: 100px;
            object-fit: cover;
            cursor: pointer;
            border-radius: 5px;
            transition: transform 0.2s;
        }
        .gallery-img:hover {
            transform: scale(1.05);
        }
        .modal-background {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.8);
        }
        .modal-content {
            position: relative;
            margin: auto;
            padding: 20px;
            width: 80%;
            max-width: 800px;
            top: 50%;
            transform: translateY(-50%);
        }
        .modal-img {
            width: 100%;
            height: auto;
        }
        .close-button {
            position: absolute;
            top: 10px;
            right: 25px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
    """

    # --- HTML Structure ---
    # Cria a grelha de imagens e a estrutura do modal
    images_html = "".join([f'<img src="{url}" class="gallery-img" onclick="openModal_{key_prefix}(\'{url}\')">' for url in image_urls])
    html_structure = f"""
    <div class="gallery-container">{images_html}</div>
    <div id="myModal_{key_prefix}" class="modal-background" onclick="closeModal_{key_prefix}()">
        <span class="close-button" onclick="closeModal_{key_prefix}()">×</span>
        <div class="modal-content">
            <img id="modalImg_{key_prefix}" class="modal-img">
        </div>
    </div>
    """

    # --- JavaScript Logic ---
    # Funções para abrir/fechar o modal e definir a imagem
    js_logic = f"""
    <script>
        var modal_{key_prefix} = document.getElementById("myModal_{key_prefix}");
        var modalImg_{key_prefix} = document.getElementById("modalImg_{key_prefix}");

        function openModal_{key_prefix}(imgSrc) {{
            modal_{key_prefix}.style.display = "block";
            modalImg_{key_prefix}.src = imgSrc;
        }}

        function closeModal_{key_prefix}() {{
            modal_{key_prefix}.style.display = "none";
        }}
        
        // Fecha o modal se o utilizador clicar fora da imagem
        window.onclick = function(event) {{
            if (event.target == modal_{key_prefix}) {{
                closeModal_{key_prefix}();
            }}
        }}
    </script>
    """

    # Combina tudo e retorna o componente HTML
    full_html = css_styles + html_structure + js_logic
    
    # Calcula uma altura razoável para o container da grelha
    # Aprox. 120px por linha para uma grelha de 3 colunas
    num_rows = -(-len(image_urls) // 3)  # Ceiling division
    height = num_rows * 120
    
    return components.html(full_html, height=height)