// eslint-disable-next-line no-unused-vars
import React, {useState} from 'react';
import './MenuBar.css';
import PropTypes from "prop-types";

const MenuBar = ({ onSelect }) => {

    const handleSelectChange = (option) => {
        onSelect(option);
    };

    return (
        <div className="menu-bar">
            <ul className="menu-list">
                <button className="menu-item" onClick={() => handleSelectChange("WORLD")}>World</button>
                <button className="menu-item" onClick={() => handleSelectChange("NATION")}>United States</button>
                <button className="menu-item" onClick={() => handleSelectChange("BUSINESS")}>Business</button>
                <button className="menu-item" onClick={() => handleSelectChange("TECHNOLOGY")}>Technology</button>
                <button className="menu-item" onClick={() => handleSelectChange("ENTERTAINMENT")}>Entertainment</button>
                <button className="menu-item" onClick={() => handleSelectChange("SPORTS")}>Sports</button>
                <button className="menu-item" onClick={() => handleSelectChange("SCIENCE")}>Science</button>
                <button className="menu-item" onClick={() => handleSelectChange("HEALTH")}>Health</button>
            </ul>
        </div>
    );
};

MenuBar.propTypes = {
    onSelect: PropTypes.func.isRequired,
};

export default MenuBar;