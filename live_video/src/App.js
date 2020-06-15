/* Let CRA handle linting for sample app */

import React, { Component } from 'react';
import Spinner from 'react-spinner';
import classNames from 'classnames';

import AccCore from 'opentok-accelerator-core';
import 'opentok-solutions-css';

import logo from './logo.svg';
import config from './config.json';
import './App.css';
import axios from 'axios';

import { withRouter } from 'react-router-dom';
import queryString from 'query-string';

let otCore;


/**
 * Build classes for container elements based on state
 * @param {Object} state
 */
const containerClasses = (state) => {
  const { active, meta, localAudioEnabled, localVideoEnabled } = state;
  const sharingScreen = meta ? !!meta.publisher.screen : false;
  const viewingSharedScreen = meta ? meta.subscriber.screen : false;
  const activeCameraSubscribers = meta ? meta.subscriber.camera : 0;
  const activeCameraSubscribersGt2 = activeCameraSubscribers > 2;
  const activeCameraSubscribersOdd = activeCameraSubscribers % 2;
  const screenshareActive = viewingSharedScreen || sharingScreen;
  return {
    controlClass: classNames('App-control-container', { hidden: !active }),
    localAudioClass: classNames('ots-video-control circle audio', { hidden: !active, muted: !localAudioEnabled }),
    localVideoClass: classNames('ots-video-control circle video', { hidden: !active, muted: !localVideoEnabled }),
    localCallClass: classNames('ots-video-control circle end-call', { hidden: !active }),
    cameraPublisherClass: classNames('video-container', { hidden: !active, small: !!activeCameraSubscribers || screenshareActive, left: screenshareActive }),
    screenPublisherClass: classNames('video-container', { hidden: !active || !sharingScreen }),
    cameraSubscriberClass: classNames('video-container', { hidden: !active || !activeCameraSubscribers },
      { 'active-gt2': activeCameraSubscribersGt2 && !screenshareActive },
      { 'active-odd': activeCameraSubscribersOdd && !screenshareActive },
      { small: screenshareActive }
    ),
    screenSubscriberClass: classNames('video-container', { hidden: !viewingSharedScreen || !active }),
  };
};


const connectingMask = () =>
  <div className="App-mask">
    <Spinner />
    <div className="message with-spinner">Connecting</div>
  </div>;

const startCallMask = start =>
  <div className="App-mask">
    <button className="message button clickable" onClick={start}>Click to Start </button>
  </div>;

const studentInfo = students =>
<div>
    {students.map((obj, key) => {
                  let student_id = obj.id;
                  return (
                      <div>
                          <p>Ученик: {obj.name} / количество бонусов: {obj.reward_card_amount}</p>
                        <button onClick={() => {
                                let url = "http://185.185.69.2:8000/students/api/0/set-reward-card/" + obj.id + '/6/0/';
                                axios.get(url)
                                      .then((response) => {
                                          console.log(response.data);
                                      })
                                      .catch((err) => {
                                          console.log(err);
                                          //this.setState({ data: err, isLoading: false });
                                      });
                              }}> +
                              бонус
                          </button>
                      </div>
                  )
              })
          }
</div>;


function Cards(props) {
    console.log(props.students);

      return (
          <div>
              {props.students.map((obj, key) => {
                  let student_id = obj.id;
                  return (
                      <div>
                          <p>Ученик: {obj.name} / количество бонусов: {obj.reward_card_amount}</p>
                          <button onClick={() => {
                              let url = "http://185.185.69.2:8000/students/api/0/set-reward-card/" + obj.id + '/6/0/';
                              axios.get(url)
                                  .then((response) => {
                                      console.log(response.data);
                                  })
                                  .catch((err) => {
                                      console.log(err);
                                      //this.setState({ data: err, isLoading: false });
                                  });
                          }}> +
                              бонус
                          </button>
                      </div>
                  )
              })
              }
          </div>
      )

}



class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      connected: false,
      active: false,
      publishers: null,
      subscribers: null,
      meta: null,
      localAudioEnabled: true,
      localVideoEnabled: true,
      token: 0,
      session_id: 0,
      students: [],
      lesson_id: 0,
      student: false,
    };
    this.startCall = this.startCall.bind(this);
    this.endCall = this.endCall.bind(this);
    this.toggleLocalAudio = this.toggleLocalAudio.bind(this);
    this.toggleLocalVideo = this.toggleLocalVideo.bind(this);
  }

  componentDidMount() {

      let query = queryString.parse(window.location.search);
      let request_url = 'http://185.185.69.2:8000/students/api/0/get-lesson-info/' + query.lesson_id + '/';

      axios.get(request_url)
          .then((response) => {
              this.setState({token: response.data.token});
              this.setState({sessionId: response.data.session_id});
              this.setState({student: query.student});
              if(this.state.student === 'false'){
                    this.setState({students: response.data.students});
              }
              this.setState({lesson_id: response.data.id});

              const otCoreOptions = {
                  credentials: {
                      apiKey: config.apiKey,
                      sessionId: this.state.sessionId,
                      token: this.state.token,
                  },
                  // A container can either be a query selector or an HTML Element
                  streamContainers(pubSub, type, data, stream) {
                      return {
                          publisher: {
                              camera: '#cameraPublisherContainer',
                              screen: '#screenPublisherContainer',
                          },
                          subscriber: {
                              camera: '#cameraSubscriberContainer',
                              screen: '#screenSubscriberContainer',
                          },
                      }[pubSub][type];
                  },
                  controlsContainer: '#controls',
                  packages: ['textChat', 'screenSharing', 'annotation'],
                  communication: {
                      callProperties: null, // Using default
                  },
                  textChat: {
                      name: ['David', 'Paul', 'Emma', 'George', 'Amanda'][Math.random() * 5 | 0], // eslint-disable-line no-bitwise
                      waitingMessage: 'Messages will be delivered when other users arrive',
                      container: '#chat',
                  },
                  screenSharing: {
                      extensionID: 'plocfffmbcclpdifaikiikgplfnepkpo',
                      annotation: true,
                      externalWindow: false,
                      dev: true,
                      screenProperties: {
                          insertMode: 'append',
                          width: '100%',
                          height: '100%',
                          showControls: false,
                          style: {
                              buttonDisplayMode: 'off',
                          },
                          videoSource: 'window',
                          fitMode: 'contain' // Using default
                      },
                  },
                  annotation: {
                      absoluteParent: {
                          publisher: '.App-video-container',
                          subscriber: '.App-video-container'
                      }
                  },
              };

              otCore = new AccCore(otCoreOptions);
              otCore.connect().then(() => this.setState({connected: true}));
              const events = [
                  'subscribeToCamera',
                  'unsubscribeFromCamera',
                  'subscribeToScreen',
                  'unsubscribeFromScreen',
                  'startScreenShare',
                  'endScreenShare',
              ];

              events.forEach(event => otCore.on(event, ({publishers, subscribers, meta}) => {
                  this.setState({publishers, subscribers, meta});
              }));

          });
  }
  startCall() {
    otCore.startCall()
      .then(({ publishers, subscribers, meta }) => {
        this.setState({ publishers, subscribers, meta, active: true });
      }).catch(error => console.log(error));
  }

  endCall() {
    otCore.endCall();
    this.setState({ active: false });
  }

  toggleLocalAudio() {
    otCore.toggleLocalAudio(!this.state.localAudioEnabled);
    this.setState({ localAudioEnabled: !this.state.localAudioEnabled });
  }

  toggleLocalVideo() {
    otCore.toggleLocalVideo(!this.state.localVideoEnabled);
    this.setState({ localVideoEnabled: !this.state.localVideoEnabled });
  }

  render() {
    const { connected, active, session_id, token, students, lesson_id, student } = this.state;
    const {
      localAudioClass,
      localVideoClass,
      localCallClass,
      controlClass,
      cameraPublisherClass,
      screenPublisherClass,
      cameraSubscriberClass,
      screenSubscriberClass,
    } = containerClasses(this.state);

      return (
      <div className="App">
        <div className="App-header">
          <img src="http://127.0.0.1:8000/static/images/logo-rus.png" className="App-logo" alt="logo" />
          <h1>Гарантия Знаний</h1>
        </div>
        <div className="App-main">
          <Cards students={students}/>
          <div className="App-video-container">
            { !connected && connectingMask() }
            { connected && !active && startCallMask(this.startCall)}
            <div id="cameraPublisherContainer" className={cameraPublisherClass} />
            <div id="screenPublisherContainer" className={screenPublisherClass} />
            <div id="cameraSubscriberContainer" className={cameraSubscriberClass} />
            <div id="screenSubscriberContainer" className={screenSubscriberClass} />
          </div>
          <div id="controls" className={controlClass}>
            <div className={localAudioClass} onClick={this.toggleLocalAudio} />
            <div className={localVideoClass} onClick={this.toggleLocalVideo} />
            <div className={localCallClass} onClick={this.endCall} />
          </div>
          <div id="chat" className="App-chat-container" />
        </div>
      </div>
    );
  }
}

export default App;
