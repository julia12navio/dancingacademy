odoo.define('dancingacademy.youtube_player', function (require) {
    "use strict";

    const AbstractField = require('web.AbstractField');

    const YouTubePlayer = AbstractField.extend({
        events: {
            'click .play-video': '_onPlayVideo',
        },

        _onPlayVideo: function (ev) {
            ev.preventDefault();
            const videoUrl = $(ev.currentTarget).data('video-url');
            const iframe = $('#youtube_video_player iframe');
            iframe.attr('src', videoUrl.replace("watch?v=", "embed/"));
        },
    });

    return YouTubePlayer;
});

