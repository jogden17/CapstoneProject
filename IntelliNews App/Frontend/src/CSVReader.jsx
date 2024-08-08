import { useEffect, useState } from 'react';
import Papa from 'papaparse';
/* masonry found here: https://github.com/desandro/masonry */
import Masonry from 'react-masonry-css';
import PropTypes from 'prop-types';
import './CSVReader.css';

const CSVReader = ({ selectedOption }) => {
    const [data, setData] = useState([]);
    // /Users/jogden/Desktop/Capstone/IntelliNews/Data/BUSINESS_Final.csv

    useEffect(() => {
        fetch(`/CSVs/${selectedOption}_Final.csv`)
            .then(response => response.text())
            .then(text => {
                Papa.parse(text, {
                    header: true,
                    complete: (results) => {
                        setData(results.data);
                    },
                    skipEmptyLines: true,
                });
            });
    }, [selectedOption]);

    // Define breakpoint columns for Masonry
    const breakpointColumnsObj = {
        default: 2,
        900: 1
    };

    // Function to render URLs as clickable links
    const renderLinks = (linkString) => {
        if (!linkString) return null;
        let hold = linkString.split("'")
        linkString = hold.join("")
        linkString = linkString.replace("[","").replace("]","")
        const urls = linkString.split(', ').map(url => url.trim());
        return (
            <span>
                {urls.map((url, index) => (
                    <a href={url} key={index} target="_blank" rel="noopener noreferrer">
                        [{index+1}]&nbsp;
                    </a>
                ))}
            </span>
        );
    };

    return (
        <div>
            <p className="categoryName">&nbsp;{selectedOption}&nbsp;</p>
            <Masonry
                breakpointCols={breakpointColumnsObj}
                className="my-masonry-grid"
                columnClassName="my-masonry-grid_column">
                {data.map((row, index) => (
                    <div key={index} className="grid-item">
                        <p className="headline">{Object.entries(row)[0][1]}</p>
                        <p className="summary">{Object.entries(row)[1][1]}</p>
                        <p className="links">Further Reading: {renderLinks(Object.entries(row)[2][1])}</p>
                    </div>
                ))}
            </Masonry>
        </div>
    );
};

CSVReader.propTypes = {
    selectedOption: PropTypes.string.isRequired,
};

export default CSVReader;
