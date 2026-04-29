import { Link } from 'react-router-dom';
import logo from './logo.svg';
import './Main.css';

function Main(){

	return(
		<div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          AI 사이트에 오신걸 환영합니다.
        </p>
        <Link
          className="App-link"
          to={"/list"}
        >
          사이트로 이동
        </Link>
      </header>
    </div>
	)
}

export default Main