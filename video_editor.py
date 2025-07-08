import streamlit as st
from moviepy.editor import *
from PIL import Image
import numpy as np
import re
from datetime import datetime

st.set_page_config(layout="wide")
st.title("Editor de Vídeo para Reels do Instagram")

def sort_images_numerically(files):
    """Ordena uma lista de arquivos com base em um número no início do nome."""
    if not files:
        return []
    
    def get_number(file):
        # Extrai o número do início do nome do arquivo para usar como chave de ordenação.
        match = re.match(r'(\d+)', file.name)
        if match:
            return int(match.group(1))
        # Retorna um número muito grande para arquivos sem prefixo numérico,
        # garantindo que eles fiquem no final da lista.
        return float('inf')

    return sorted(files, key=get_number)


# --- Lógica de Geração de Vídeo ---

def create_base_clip(images, duration_per_image, total_duration, size=(1080, 1920)):
    """Cria o clipe de vídeo base a partir das imagens, com loop se necessário."""
    if not images:
        return ColorClip(size, color=(0, 0, 0), duration=total_duration)
    
    clips = []
    for img_file in images:
        img = Image.open(img_file).convert("RGB")
        img_resized = img.resize(size, Image.Resampling.LANCZOS)
        clip = ImageClip(np.array(img_resized)).set_duration(duration_per_image)
        clips.append(clip)
    
    if not clips: # Segurança extra
        return ColorClip(size, color=(0, 0, 0), duration=total_duration)

    single_sequence = concatenate_videoclips(clips, method="compose")
    
    if single_sequence.duration > 0 and single_sequence.duration < total_duration:
        num_loops = int(total_duration / single_sequence.duration) + 1
        final_clips = clips * num_loops
        final_video = concatenate_videoclips(final_clips, method="compose")
    else:
        final_video = single_sequence
        
    return final_video.set_duration(total_duration)

def add_overlay_image(video_clip, overlay_file, pos_x, pos_y, size, opacity):
    """Adiciona uma imagem de sobreposição (logo ou outra) ao vídeo."""
    if not overlay_file:
        return video_clip

    overlay_img = Image.open(overlay_file)
    
    new_height = int(overlay_img.height * size)
    new_width = int(overlay_img.width * (new_height / overlay_img.height))
    overlay_resized = overlay_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    overlay_clip = (ImageClip(np.array(overlay_resized))
                    .set_duration(video_clip.duration)
                    .set_opacity(opacity)
                    .set_pos((pos_x, pos_y)))
    
    return CompositeVideoClip([video_clip, overlay_clip])

def add_scrolling_caption(video_clip, caption_file, y_pos, speed, fontsize, color, font, loop):
    """Adiciona a legenda com efeito de letreiro."""
    if not caption_file:
        return video_clip

    caption_file.seek(0)
    text = caption_file.read().decode("utf-8").replace("\n", " | ")
    
    txt_clip_info = TextClip(text, fontsize=fontsize, color=color, font=font)
    txt_w = txt_clip_info.size[0]
    video_w = video_clip.size[0]

    def scroll_text(t):
        effective_speed = speed * 50
        if loop:
            x_pos = video_w - (effective_speed * t) % (video_w + txt_w)
        else:
            x_pos = video_w - (effective_speed * t)
        return (x_pos, y_pos)

    text_clip = (TextClip(text, fontsize=fontsize, color=color, font=font)
                 .set_position(scroll_text)
                 .set_duration(video_clip.duration))
    
    return CompositeVideoClip([video_clip, text_clip])

def add_static_caption_for_preview(video_clip, caption_file, y_pos, fontsize, color, font):
    """Adiciona uma legenda estática para o preview."""
    if not caption_file:
        return video_clip

    caption_file.seek(0)
    text = caption_file.read().decode("utf-8").replace("\n", " | ")
    
    text_clip = (TextClip(text, fontsize=fontsize, color=color, font=font, size=(video_clip.w, None), method='caption', align='center')
                 .set_position(('center', y_pos))
                 .set_duration(video_clip.duration))
    
    return CompositeVideoClip([video_clip, text_clip])

def generate_final_video():
    """Função principal que monta o vídeo com todos os elementos."""
    video = create_base_clip(uploaded_images, image_duration, total_duration)
    
    if uploaded_logo:
        video = add_overlay_image(video, uploaded_logo, logo_x, logo_y, logo_size, logo_opacity)
    
    if uploaded_overlay:
        video = add_overlay_image(video, uploaded_overlay, overlay_x, overlay_y, overlay_size, overlay_opacity)
        
    if uploaded_captions:
        video = add_scrolling_caption(video, uploaded_captions, caption_y, caption_speed, caption_fontsize, caption_color, caption_font, caption_loop)
        
    return video


def generate_preview_frame(base_image, logo_file, overlay_file, caption_file, **kwargs):
    """
    Gera um único frame de preview com base nos arquivos e configurações fornecidas.
    Isso permite atualizações reativas na interface.
    """
    PREVIEW_SCALE = 0.5
    PREVIEW_SIZE = (int(1080 * PREVIEW_SCALE), int(1920 * PREVIEW_SCALE))

    # Usa a primeira imagem como base para o preview
    preview_clip = create_base_clip([base_image], 1, 1, size=PREVIEW_SIZE)

    if logo_file:
        preview_clip = add_overlay_image(
            preview_clip, logo_file,
            int(kwargs.get('logo_x', 0) * PREVIEW_SCALE),
            int(kwargs.get('logo_y', 0) * PREVIEW_SCALE),
            kwargs.get('logo_size', 0.5) * PREVIEW_SCALE,
            kwargs.get('logo_opacity', 1.0)
        )
    
    if overlay_file:
        preview_clip = add_overlay_image(
            preview_clip, overlay_file,
            int(kwargs.get('overlay_x', 0) * PREVIEW_SCALE),
            int(kwargs.get('overlay_y', 0) * PREVIEW_SCALE),
            kwargs.get('overlay_size', 0.8) * PREVIEW_SCALE,
            kwargs.get('overlay_opacity', 1.0)
        )
    
    if caption_file:
        preview_clip = add_static_caption_for_preview(
            preview_clip, caption_file,
            int(kwargs.get('caption_y', 1700) * PREVIEW_SCALE),
            int(kwargs.get('caption_fontsize', 50) * PREVIEW_SCALE),
            kwargs.get('caption_color', '#FFFFFF'),
            kwargs.get('caption_font', 'Liberation-Sans-Bold')
        )

    return preview_clip.get_frame(0)


# --- Layout da Interface ---
controls_col, preview_col = st.columns([3, 2])

with controls_col:
    st.header("1. Controles")

    with st.expander("Arquivos", expanded=True):
        uploaded_logo = st.file_uploader("Logo (PNG)", type="png")
        uploaded_overlay = st.file_uploader("Imagem de Sobreposição (PNG)", type="png")
        uploaded_images_raw = st.file_uploader("Imagens de Fundo (JPG/PNG)", type=["jpg", "png"], accept_multiple_files=True)
        uploaded_images = sort_images_numerically(uploaded_images_raw)
        uploaded_captions = st.file_uploader("Arquivo de Legendas (.txt)", type="txt")
        uploaded_audio = st.file_uploader("Trilha Sonora (MP3/WAV)", type=["mp3", "wav"])

    with st.expander("Configurações Gerais", expanded=True):
        total_duration = st.slider("Duração total do Reel (segundos)", 15, 90, 15)
        image_duration = st.number_input("Duração de cada imagem (segundos)", min_value=0.1, value=2.0, step=0.1)

    with st.expander("Opções da Logo"):
        if uploaded_logo:
            logo_x = st.slider("Posição X da Logo", 0, 1080, 50)
            logo_y = st.slider("Posição Y da Logo", 0, 1920, 50)
            logo_size = st.slider("Tamanho da Logo", 0.1, 2.0, 0.5, 0.1)
            logo_opacity = st.slider("Transparência da Logo", 0.0, 1.0, 1.0, 0.1)

    with st.expander("Opções da Sobreposição"):
        if uploaded_overlay:
            overlay_x = st.slider("Posição X da Sobreposição", 0, 1080, 800)
            overlay_y = st.slider("Posição Y da Sobreposição", 0, 1920, 1500)
            overlay_size = st.slider("Tamanho da Sobreposição", 0.1, 2.0, 0.8, 0.1)
            overlay_opacity = st.slider("Transparência da Sobreposição", 0.0, 1.0, 1.0, 0.1)

    with st.expander("Opções da Legenda"):
        if uploaded_captions:
            caption_y = st.slider("Posição Y da Legenda", 0, 1920, 1700)
            caption_speed = st.slider("Velocidade da Legenda", 1, 20, 5)
            caption_fontsize = st.slider("Tamanho da Fonte", 10, 100, 50)
            caption_color = st.color_picker("Cor da Fonte", "#FFFFFF")
            # Removendo a seleção de fonte para evitar erros de fontes não encontradas.
            # Usando uma fonte fixa que é conhecida por funcionar neste ambiente.
            caption_font = "Liberation-Sans-Bold"
            st.info(f"Fonte da legenda foi fixada em '{caption_font}' para garantir a compatibilidade.")
            caption_loop = st.checkbox("Habilitar loop na legenda", value=True)

    st.header("2. Gerar Vídeo Final")

    # Inicializa o session_state para o nome do arquivo se ele não existir
    if 'final_filename' not in st.session_state:
        st.session_state.final_filename = f"reel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

    # O valor do input é agora controlado pelo session_state
    st.text_input(
        "Nome do arquivo de vídeo:",
        key='final_filename' # Usar a chave para vincular ao session_state
    )

    if st.button("Gerar Vídeo"):
        if not uploaded_images:
            st.error("Por favor, faça o upload de pelo menos uma imagem de fundo.")
        elif not st.session_state.final_filename.endswith(".mp4"):
            st.error("O nome do arquivo deve terminar com .mp4")
        else:
            with st.spinner("Gerando vídeo... Isso pode levar alguns minutos."):
                final_video = generate_final_video()
                
                if uploaded_audio:
                    # Usar um nome temporário para o áudio para evitar conflitos
                    temp_audio_path = "temp_audio_for_processing.mp3"
                    with open(temp_audio_path, "wb") as f:
                        f.write(uploaded_audio.getbuffer())
                    
                    audio_clip = AudioFileClip(temp_audio_path)
                    if audio_clip.duration > final_video.duration:
                        audio_clip = audio_clip.subclip(0, final_video.duration)
                    
                    final_video = final_video.set_audio(audio_clip)

                final_clip_path = st.session_state.final_filename
                final_video.write_videofile(final_clip_path, fps=24, codec='libx264', audio_codec='aac')
                
                st.success("Vídeo gerado com sucesso!")
                st.video(final_clip_path)
                with open(final_clip_path, "rb") as file:
                    st.download_button(
                        label="Baixar Vídeo",
                        data=file,
                        file_name=final_clip_path, # Usar o nome do arquivo final
                        mime="video/mp4"
                    )

# --- Lógica do Preview na Coluna Lateral ---
with preview_col:
    st.header("Preview")
    
    # A lógica do preview agora é reativa. Ele será atualizado sempre que um controle for alterado.
    if uploaded_images:
        # Coleta os parâmetros atuais dos widgets para passar para a função de preview.
        # A verificação 'in locals()' evita erros se um arquivo for enviado e depois removido.
        preview_params = {
            'logo_x': logo_x if 'logo_x' in locals() else 0,
            'logo_y': logo_y if 'logo_y' in locals() else 0,
            'logo_size': logo_size if 'logo_size' in locals() else 0.5,
            'logo_opacity': logo_opacity if 'logo_opacity' in locals() else 1.0,
            'overlay_x': overlay_x if 'overlay_x' in locals() else 0,
            'overlay_y': overlay_y if 'overlay_y' in locals() else 0,
            'overlay_size': overlay_size if 'overlay_size' in locals() else 0.8,
            'overlay_opacity': overlay_opacity if 'overlay_opacity' in locals() else 1.0,
            'caption_y': caption_y if 'caption_y' in locals() else 1700,
            'caption_fontsize': caption_fontsize if 'caption_fontsize' in locals() else 50,
            'caption_color': caption_color if 'caption_color' in locals() else '#FFFFFF',
            'caption_font': caption_font if 'caption_font' in locals() else 'Liberation-Sans-Bold',
        }
        
        with st.spinner("Atualizando preview..."):
            # Gera e exibe o frame de preview em tempo real
            preview_frame = generate_preview_frame(
                uploaded_images[0],
                uploaded_logo,
                uploaded_overlay,
                uploaded_captions,
                **preview_params
            )
            st.image(preview_frame, caption="Preview da Composição", use_container_width=True)
    else:
        st.info("Faça o upload de pelo menos uma imagem para visualizar o preview.")
