function View() {
    var self = this;

    /////////////////////////////////////////
    // Public members
    /////////////////////////////////////////

    self.StageEnum = {
        PLAY_PROMPT : $("#play_prompt"),
        INFORMATION_PROMPT : $("#information_prompt"),
        EXCHANGE_PROMPT : $("#exchange_prompt"),
        WAIT_PROMPT : $("#wait_prompt"),
    }

    self.current_stage = self.StageEnum.INFORMATION_PROMPT;
    self.context = document.getElementById("canvas").getContext("2d");
    self.game = null;
    self.table_width = 1024;
    self.table_height = 768;

    /////////////////////////////////////////
    // Private constants
    /////////////////////////////////////////

    var RENDER_DELAY = 15;
    var CARDS = ["1s",  "1c",  "1d",  "1h",
                 "2s",  "2c",  "2d",  "2h",
                 "3s",  "3c",  "3d",  "3h",
                 "4s",  "4c",  "4d",  "4h",
                 "5s",  "5c",  "5d",  "5h",
                 "6s",  "6c",  "6d",  "6h",
                 "7s",  "7c",  "7d",  "7h",
                 "8s",  "8c",  "8d",  "8h",
                 "9s",  "9c",  "9d",  "9h",
                 "10s", "10c", "10d", "10h",
                 "11s", "11c", "11d", "11h",
                 "12s", "12c", "12d", "12h",
                 "13s", "13c", "13d", "13h"];


    /////////////////////////////////////////
    // Private members
    /////////////////////////////////////////

    var background_picture = null;
    var card_images = new Array();
    var request_animation_frame = (function (callback, element) {
        var f =
            window.webkitRequestAnimationFrame ||
            window.mozRequestAnimationFrame ||
            window.oRequestAnimationFrame ||
            window.msRequestAnimationFrame ||
            function (callback,element) {
                window.setTimeout(callback, 1000 / 60); // Fallback timeout
            };
        return f;
    })();

    /////////////////////////////////////////
    // Private Functions
    /////////////////////////////////////////

    function render_seat1() {
        if (self.game) {
            for (var i = 0; i < 13; ++i) {
                if (true || self.game.seats[0].cards[i]) {
                    context.drawImage(
                        card_images[self.game.seats[0].cards[i]],
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        100,
                        100);
                }
            }
        }
    }

    function render_seat2() {
        if (self.game) {
        }
    }

    function render_seat3() {
        if (self.game) {
        }
    }

    function render_seat4() {
        if (self.game) {
        }
    }

    function render_table() {
        render_seat1();
        render_seat2();
        render_seat3();
        render_seat4();
    }

    function render() {
        //window.document.body.style.backgroundImage = "url(./images/background.png)";

        $("#play_prompt").hide();
        $("#information_prompt").hide();
        $("#exchange_prompt").hide();
        $("#wait_prompt").hide();

        self.current_stage.css("display", "table");
    }

    function animate() {
        request_animation_frame(animate, null);
        render();
    }

    function load_images() {
        background_picture = load_image("./images/background.png");
        for (var i = 0; i < CARDS.length; i++) {
            card_images[i] = load_image("./decks/anglo/5/" + CARDS[i] + ".gif");
        }
    }

    function load_image(img_src) {
        var image = new Image ();
        image.src = img_src;
        image.is_loaded = false;
        image.onload = function () {
            this.is_loaded = true;
        };

        return image;
    }

    /////////////////////////////////////////
    // Main
    /////////////////////////////////////////

    load_images();
    render_table();
    animate();
}
