// Initialize an OpenTok Session object
var session = OT.initSession(apiKey, sessionId);

// Initialize a Publisher, and place it into the element with id="publisher"
//var publisher = OT.initPublisher('publisher');




session.connect(token, function(error) {
  if (error) {
    console.log(error.message);
  } else {

    var publisherOptions = {width: 400, height:300, name:"Bob's stream"};
    // This assumes that there is a DOM element with the ID 'publisher':
    OT.checkScreenSharingCapability(function(response) {
  if(!response.supported || response.extensionRegistered === false) {
    // This browser does not support screen sharing.
  } else if (response.extensionInstalled === false) {
    // Prompt to install the extension.
  } else {
    // Screen sharing is available. Publish the screen.
    var publisher = OT.initPublisher('screen-preview',
      {videoSource: 'screen'},
      function(error) {
        if (error) {
          // Look at error.message to see what went wrong.
            alert(error.message);
        } else {
          session.publish(publisher, function(error) {
            if (error) {
              // Look error.message to see what went wrong.
                 alert("erroe 2");
            }
          });
        }
      }
    );
  }
});

    session.publish(publisher, function(error) {
  if (error) {
    console.log(error);
  } else {
    console.log('Publishing a stream.');
  }
});
publisher.on('streamCreated', function (event) {
    console.log('The publisher started streaming.');
});
  }
});
