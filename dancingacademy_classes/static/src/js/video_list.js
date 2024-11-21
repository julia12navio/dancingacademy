odoo.define('dancingacademy.VideoList', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');

    publicWidget.registry.VideoListWidget = publicWidget.Widget.extend({
        selector: '#videoListContainer',
        start: function () {
            const videosList = JSON.parse(this.$el.attr('data-videos')); // Obtiene los datos desde el atributo
            const container = this.$('.video-container');
            const noVideosMessage = this.$('#noVideosMessage');

            if (videosList && videosList.length > 0) {
                videosList.forEach(video => {
                    const videoItem = `
                        <li class="video-item">
                            <a href="${video.url}" target="_blank">
                                <img src="${video.thumbnail}" alt="Thumbnail" />
                                <p>${video.title}</p>
                            </a>
                        </li>`;
                    container.append(videoItem);
                });
            } else {
                noVideosMessage.show();
            }
        },
    });
});
