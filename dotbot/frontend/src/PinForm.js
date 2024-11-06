import mqtt from 'mqtt';
import './QrKeyForm.css';

export const QrKeyForm = ({ mqttDataUpdate }) => {

  const [pinCode, setPinCode] = useState(null);
  const [mqttHost, setMqttHost] = useState(null);
  const [mqttPort, setMqttPort] = useState(null);
  const [mqttVersion, setMqttVersion] = useState(null);
  const [mqttUseSSL, setMqttUseSSL] = useState(true);
  const [mqttUsername, setMqttUsername] = useState(null);
  const [mqttPassword, setMqttPassword] = useState(null);

  const onInputPinChange = (event) => {
    if (event.target.value.length === parseInt(process.env.REACT_APP_PIN_CODE_LENGTH)) {
      setPinCode(event.target.value);
    }
  };

  const onInputMqttHostChange = (event) => {
    setMqttHost(event.target.value);
  };

  const onInputMqttPortChange = (event) => {
    setMqttPort(parseInt(event.target.value));
  };

  const onInputMqttVersionChange = (event) => {
    setMqttVersion(parseInt(event.target.value));
  };

  const onInputMqttUseSSLChange = (event) => {
    setMqttUseSSL(event.target.value);
  };

  const onInputMqttUsernameChange = (event) => {
    setMqttUsername(event.target.value);
  };

  const onInputMqttPasswordChange = (event) => {
    setMqttPassword(event.target.value);
  };

  const connect = () => {
    const mqttData = {
      pin_code: pinCode,
      mqtt_host: mqttHost,
      mqtt_port: mqttPort,
      mqtt_version: mqttVersion,
      mqtt_use_ssl: mqttUseSSL,
      mqtt_username: mqttUsername,
      mqtt_password: mqttPassword,
    };
    console.log(`Connect: ${JSON.stringify(mqttData)}`);
    mqttDataUpdate(mqttData);
  };

  const buttonDisabled = pinCode === null || pinCode.length !== parseInt(process.env.REACT_APP_PIN_CODE_LENGTH) || mqttHost === null || mqttPort === null || mqttVersion === null;

  return (
    <div className="container">
      <form id="form-input">
        <p>Enter pin code:</p>
        <p>
          <input type="password" className="form-control" placeholder="Pin Code" autoFocus="autofocus" onChange={(event) => onInputPinChange(event)} />
        </p>
        <p>
          <input type="text" className="form-control" placeholder="MQTT Host" required onChange={(event) => onInputMqttHostChange(event)} />
        </p>
        <p>
          <input type="number" className="form-control" placeholder="MQTT Websocket Port" required onChange={(event) => onInputMqttPortChange(event)} />
        </p>
        <p>
          <input type="number" className="form-control" placeholder="MQTT Version" required value="5" onChange={(event) => onInputMqttVersionChange(event)} />
        </p>
        <p>
          <div className="form-check">
            <input className="form-check-input" type="checkbox" id="useSSLCheck" checked onChange={(event) => onInputMqttUseSSLChange(event)} />
            <label className="form-check-label" for="useSSLCheck">
              Use SSL
            </label>
          </div>
        </p>
        <p>
          <input type="text" className="form-control" placeholder="MQTT username (optional)" onChange={(event) => onInputMqttUsernameChange(event)} />
        </p>
        <p>
          <input type="password" className="form-control" placeholder="MQTT password (optional)" onChange={(event) => onInputMqttPasswordChange(event)} />
        </p>
        <p>
          <button class="btn btn-light" type="submit" disabled={buttonDisabled} onClick={connect}>
            Connect
          </button>
        </p>
      </form>
    </div>
  );
};
