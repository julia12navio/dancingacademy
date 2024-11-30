odoo.define('dancingacademy_classes', function (require) {
    "use strict";

    console.log("Iniciando módulo dancingacademy_classes...");

    // Variable para rastrear si la lógica ya se ejecutó
    let currentView = null;

    // Encapsulamos la lógica principal en una función reutilizable
    function initializeLogic() {
        console.log("Inicializando lógica de la clase...");

        // Función para esperar hasta que un elemento esté disponible (con máximo 2 intentos)
        function waitForElement(selector, callback, maxAttempts = 2, attempt = 1) {
            const element = document.querySelector(selector);

            if (element) {
                callback(element); // Si el elemento existe, ejecutamos el callback
            } else if (attempt < maxAttempts) {
                console.log(`Elemento ${selector} aún no disponible, intento ${attempt} de ${maxAttempts}...`);
                setTimeout(() => waitForElement(selector, callback, maxAttempts, attempt + 1), 500); // Reintenta
            } else {
                console.error(`Elemento ${selector} no encontrado después de ${maxAttempts} intentos.`);
            }
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
                const thumbnailUrl = videoSnippet.thumbnails.medium.url;

                const videoDiv = document.createElement("div");
                videoDiv.style.flex = "0 0 auto";
                videoDiv.style.textAlign = "center";

                const img = document.createElement("img");
                img.src = thumbnailUrl;
                img.style.width = "200px";
                img.style.cursor = "pointer";

                img.addEventListener("click", function () {
                    window.open(`https://www.youtube.com/watch?v=${videoId}`, "_blank");
                });

                videoDiv.appendChild(img);
                videoGallery.appendChild(videoDiv);
            });
        }

        // Ejecutar la lógica
        handlePlaylistInput();
    }

    // Detectar cambios en el DOM al cargar nuevas vistas
    document.addEventListener('DOMContentLoaded', function () {
        const observer = new MutationObserver((mutationsList) => {
            mutationsList.forEach((mutation) => {
                if (mutation.addedNodes.length > 0) {
                    const content = document.querySelector('.o_form_view'); // Cambia este selector si es necesario
                    if (content && content !== currentView) {
                        console.log("Cambio de vista detectado, inicializando lógica...");
                        currentView = content; // Actualizamos la vista actual
                        initializeLogic(); // Inicializa la lógica al detectar un cambio de vista
                    }
                }
            });
        });

        // Configurar el observador para detectar cambios en el DOM
        observer.observe(document.body, { childList: true, subtree: true });

        // Ejecutar la lógica inicial
        initializeLogic();
    });
});

