$(document).ready(function() {
    // Simulated values for the sensor and battery percentage
    const batteryValue = 75; // Change this to the actual battery percentage

    // Update the sensor value and battery value on the meter screen
    document.getElementById('battery-value').textContent = batteryValue + "%";

    //GET request to the '/ultrasonic' route
    function getUltrasonicData() {
        fetch('/ultrasonic')
            .then(response => response.text())
            .then(data => {
                const sensorValueElement = document.getElementById('sensor-value');
                sensorValueElement.innerText = data;

                if (parseFloat(data) < 0.1) {
                    sensorValueElement.style.color = 'red';
                    sensorValueElement.style.fontWeight = 'bold';
                } else {
                    sensorValueElement.style.color = ''; // Reset color
                    sensorValueElement.style.fontWeight = ''; // Reset font weight
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // getUltrasonicData function every 1 second
    setInterval(getUltrasonicData, 1000);

    // Toggle video button click handler
    $("#toggle-video").click(function() {
        var imgDiv = $('.panel-1-left');
        if (imgDiv.css('display') !== 'none') {
            imgDiv.css('display', 'none');
        } else {
            imgDiv.css('display', 'block');
        }
    });

    // Post request on click with argument
    var postArgOnClick = function(selector, endpoint, arg) {
        return $(selector).click(function() {
            $.post(endpoint, { arg });
        });
    };

    // Post request on click without argument
    var postOnClick = function(selector, endpoint) {
        return $(selector).click(function() {
            $.post(endpoint, {});
        });
    };

    // Move motor on press
    var moveMotorOnPress = function(selector, arg) {
        return $(selector)
            .on('mousedown touchstart', function(e) {
                $(this).addClass('active-btn');
                $.post('/move', { arg });
            })
            .bind('mouseup mouseleave touchend', function() {
                $(this).removeClass('active');
                $.post('/move', { arg: "STOP" });
            });
    };

    // Move servo on press
    var moveServoOnPress = function(selector, arg) {
        return $(selector)
            .on('mousedown touchstart', function(e) {
                $(this).addClass('active-btn');
                timeOut = setInterval(function() {
                    $.post('/servo', { arg });
                }, 100);
            })
            .bind('mouseup mouseleave touchend', function() {
                $(this).removeClass('active');
                $.post('/servo', { arg: "STOP" });
            });
    };

    // Function to handle keydown events
    function handleKeyPress(event) {
        var key = event.key.toLowerCase();
        switch (key) {
            // Motor controls
            case 'w':
                $('#motor-forward-btn').addClass('active-btn');
                $.post('/move', { arg: 'FORWARD' });
                break;
            case 's':
                $('#motor-backwards-btn').addClass('active-btn');
                $.post('/move', { arg: 'BACKWARDS' });
                break;
            case 'a':
                $('#motor-left-btn').addClass('active-btn');
                $.post('/move', { arg: 'ForwardLeft' });
                break;
            case 'd':
                $('#motor-right-btn').addClass('active-btn');
                $.post('/move', { arg: 'ForwardRight' });
                break;
            case 'q':
                $('#motor-left-turn-btn').addClass('active-btn');
                $.post('/move', { arg: 'LEFT' });
                break;
            case 'e':
                $('#motor-right-turn-btn').addClass('active-btn');
                $.post('/move', { arg: 'RIGHT' });
                break;
            case ' ':
                // Stop motor
                $('.motor-btn').removeClass('active-btn');
                $.post('/move', { arg: 'STOP' });
                break;
            // Servo controls
            case 'arrowup':
                $('#servo-up-btn').addClass('active-btn');
                $.post('/servo', { arg: 'UP' });
                break;
            case 'arrowdown':
                $('#servo-down-btn').addClass('active-btn');
                $.post('/servo', { arg: 'DOWN' });
                break;
            case 'arrowleft':
                $('#servo-left-btn').addClass('active-btn');
                $.post('/servo', { arg: 'LEFT' });
                break;
            case 'arrowright':
                $('#servo-right-btn').addClass('active-btn');
                $.post('/servo', { arg: 'RIGHT' });
                break;
            case 'enter':
                // Stop servo
                $('.servo-btn').removeClass('active-btn');
                $.post('/servo', { arg: 'STOP' });
                break;
        }
    }

    // Function to handle keyup events
    function handleKeyUp(event) {
        var key = event.key.toLowerCase();
        switch (key) {
            // Motor controls
            case 'w':
                $('#motor-forward-btn').removeClass('active-btn');
                $.post('/move', { arg: 'STOP' });
                break;
            case 's':
                $('#motor-backwards-btn').removeClass('active-btn');
                $.post('/move', { arg: 'STOP' });
                break;
            case 'a':
                $('#motor-left-btn').removeClass('active-btn');
                $.post('/move', { arg: 'STOP' });
                break;
            case 'd':
                $('#motor-right-btn').removeClass('active-btn');
                $.post('/move', { arg: 'STOP' });
                break;
            case 'q':
                $('#motor-left-turn-btn').removeClass('active-btn');
                $.post('/move', { arg: 'STOP' });
                break;
            case 'e':
                $('#motor-right-turn-btn').removeClass('active-btn');
                $.post('/move', { arg: 'STOP' });
                break;
            // Servo controls
            case 'arrowup':
                $('#servo-up-btn').removeClass('active-btn');
                $.post('/servo', { arg: 'STOP' });
                break;
            case 'arrowdown':
                $('#servo-down-btn').removeClass('active-btn');
                $.post('/servo', { arg: 'STOP' });
                break;
            case 'arrowleft':
                $('#servo-left-btn').removeClass('active-btn');
                $.post('/servo', { arg: 'STOP' });
                break;
            case 'arrowright':
                $('#servo-right-btn').removeClass('active-btn');
                $.post('/servo', { arg: 'STOP' });
                break;
        }
    }

    // Bind keydown and keyup events to the document
    $(document).keydown(handleKeyPress);
    $(document).keyup(handleKeyUp);

    // Bind click events to buttons
    postOnClick('#stop-btn', '/stop');
    postArgOnClick('#speed-up-btn', '/speed', 'up');
    postArgOnClick('#speed-down-btn', '/speed', 'down');
    moveMotorOnPress('#motor-forward-btn', 'FORWARD');
    moveMotorOnPress('#motor-backwards-btn', 'BACKWARDS');
    moveMotorOnPress('#motor-left-btn', 'ForwardLeft');
    moveMotorOnPress('#motor-right-btn', 'ForwardRight');
    moveMotorOnPress('#motor-left-turn-btn', 'LEFT');
    moveMotorOnPress('#motor-right-turn-btn', 'RIGHT');
    moveServoOnPress('#servo-up-btn', 'UP');
    moveServoOnPress('#servo-down-btn', 'DOWN');
    moveServoOnPress('#servo-left-btn', 'LEFT');
    moveServoOnPress('#servo-right-btn', 'RIGHT');

});
