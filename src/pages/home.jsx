import './home.css';
import Button from '../components/button';
import logo from '../images/Logo.svg';
import peoplePic from '../images/people.png';
export default function Home() {
    return (
        <div className="home-container">
            <img src={logo} className="logo"></img> 
            <img src={peoplePic} className="people-pic"></img>
            <div className="blurb">
                <p>A grocery finance tracker suited to your needs</p>
            </div>
            <Button text="View Shopping List" isLink={true} linkLocation="shopping-list"></Button>
        </div>
    );
}
