import './button.css';
import { Link } from 'react-router-dom'; 
export default function Button({text, onClick, isLink, linkLocation}) {
    if (isLink) {
        return (
            <Link to={linkLocation} className="button">
                {text}
            </Link>
        );
    } else {
        return (
            <div className="button" onClick={onClick}>
                {text}
            </div>
        );
    }
}
