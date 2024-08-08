import { useState } from 'react';
import CSVReader from './CSVReader';
import './App.css';
import MenuBar from "./MenuBar.jsx";

function App() {
    const [selectedOption, onSelect] = useState("WORLD");

    const handleSelectChange = (option) => {
        onSelect(option);
    };

    return (
        <div className="App">
            <header className="App-header">
                <div className="in-line">
                    <section>
                        <img className="logo" src="/logo.png"/>
                    </section>
                    <section className="content">
                        <h1 className="title">IntelliNews</h1>
                    </section>
                </div>
                <section className="content">
                    <MenuBar onSelect={handleSelectChange}/>
                </section>
            </header>
            <CSVReader selectedOption={selectedOption}/>
            <footer>
                <p>&copy; 2024 IntelliNews. All rights reserved.</p>
                <nav>
                    <a href="#">About</a> |
                    <a href="#">Privacy Policy</a> |
                    <a href="#">Careers</a>
                </nav>
                <div className="social-media">
                    <a href="#"><i className="fa-brands fa-instagram"></i></a>
                    <a href="#"><i className="fa-brands fa-twitter"></i></a>
                    <a href="#"><i className="fa-brands fa-linkedin"></i></a>
                </div>
            </footer>
        </div>
    );
}

export default App;