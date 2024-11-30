odoo.define('dancingacademy_classes', function (require) {
    "use strict";

    console.log("Iniciando módulo dancingacademy_classes...");

    document.addEventListener('DOMContentLoaded', function () {
        console.log("DOM completamente cargado, iniciando lógica...");

        // Función para esperar hasta que un elemento esté disponible
        function waitForElement(selector, callback) {
            const element = document.querySelector(selector);
            if (element) {
                callback(element);
            } else {
                console.log(`Elemento ${selector} aún no disponible, reintentando...`);
                setTimeout(() => waitForElement(selector, callback), 500);
            }
        }

        // Manejar el mensaje de estado
        function handleStatusMessage() {
            waitForElement("#js_status_message", (statusMessage) => {
                console.log("Contenedor js_status_message encontrado.");
                statusMessage.textContent = " ";
                //statusMessage.style.color = "green"; // Cambiar estilo
            });
        }

        // Manejar el campo de entrada de la URL
        function handlePlaylistInput() {
            waitForElement('.o_field_widget[name="youtube_playlist_url"] input', (playlistInput) => {
                console.log("Campo de entrada de YouTube Playlist URL encontrado.");

                // Verificar si ya hay un valor en el campo al cargar la página
                if (playlistInput.value) {
                    console.log("Cargando videos desde la URL inicial...");
                    handleVideoGallery(playlistInput.value); // Cargar videos
                }

                // Escuchar cambios en la URL
                playlistInput.addEventListener('input', (event) => {
                    console.log("URL actualizada, cargando nueva galería...");
                    handleVideoGallery(event.target.value); // Actualizar videos
                });
            });
        }

        // Manejar el contenedor youtube_video_gallery
        function handleVideoGallery(playlistUrl) {
            waitForElement("#youtube_video_gallery", (videoGallery) => {
                if (playlistUrl) {
                    console.log("Contenedor youtube_video_gallery encontrado. Procesando URL...");
                    const playlistId = extractPlaylistId(playlistUrl);

                    if (!playlistId) {
                        console.error("No se pudo extraer el ID de la lista de reproducción.");
                        videoGallery.innerHTML = "<p style='color: red;'>URL inválida o sin ID de lista.</p>";
                        return;
                    }

                    console.log("ID de la lista de reproducción:", playlistId);
                    fetchYouTubeVideos(playlistId, videoGallery); // Obtener videos
                }
            });
        }

        // Extrae el ID de la lista de reproducción de la URL
        function extractPlaylistId(url) {
            const regex = /[?&]list=([^#&]+)/;
            const match = url.match(regex);
            return match ? match[1] : null;
        }

        // Obtiene los videos de la lista de reproducción desde la API de YouTube
        async function fetchYouTubeVideos(playlistId, videoGallery) {
            const apiKey = "AIzaSyBGzOTSs-XKVm-cAWzrnU_Zo0vg7L-n33w"; // Reemplaza con tu clave de API de YouTube
            const url = `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=10&playlistId=${playlistId}&key=${apiKey}`;

            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`Error en la API de YouTube: ${response.statusText}`);
                }
                const data = await response.json();
                renderVideos(data.items || [], videoGallery);
            } catch (error) {
                console.error("Error al obtener videos de YouTube:", error);
                videoGallery.innerHTML = "<p style='color: red;'>Error al cargar videos.</p>";
            }
        }

        // Renderiza los videos en el contenedor de la galería
        function renderVideos(videos, videoGallery) {
            videoGallery.innerHTML = ""; // Limpia el contenedor

            if (videos.length === 0) {
                videoGallery.innerHTML = "<p style='color: gray;'>No se encontraron videos.</p>";
                return;
            }

            videoGallery.style.display = "flex";
            videoGallery.style.overflowX = "auto";
            videoGallery.style.gap = "10px";

            videos.forEach(video => {
                const videoSnippet = video.snippet;
                if (!videoSnippet || !videoSnippet.resourceId || !videoSnippet.thumbnails || !videoSnippet.thumbnails.medium) {
                    console.warn("Estructura inesperada de video:", video);
                    return; // Salta este video si la estructura no es la esperada
                }

                const videoId = videoSnippet.resourceId.videoId;
                //const title = videoSnippet.title;
                const thumbnailUrl = videoSnippet.thumbnails.medium.url;

                const videoDiv = document.createElement("div");
                videoDiv.style.flex = "0 0 auto";
                videoDiv.style.textAlign = "center";

                const img = document.createElement("img");
                img.src = thumbnailUrl;
                //img.alt = title;
                img.style.width = "200px";
                img.style.cursor = "pointer";

                img.addEventListener("click", function () {
                    window.open(`https://www.youtube.com/watch?v=${videoId}`, "_blank");
                });

                const videoTitle = document.createElement("p");
                //videoTitle.textContent = title;
                //videoTitle.style.fontSize = "14px";

                videoDiv.appendChild(img);
                //videoDiv.appendChild(videoTitle);
                videoGallery.appendChild(videoDiv);
            });
        }

        // Ejecutar inmediatamente la lógica
        handleStatusMessage();
        handlePlaylistInput(); // Esto asegura que se ejecute directamente al cargar la página
    });
});
