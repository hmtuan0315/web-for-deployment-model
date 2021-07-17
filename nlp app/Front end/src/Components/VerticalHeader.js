import React from 'react';
import styles from '../Css/VerticalHeader.module.css'
import logo from '../assets/image/logo.jpg'
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";

function VerticalHeader(props) {
    const names = [{name: "Sentiment Analysist", url:"/"},
    {name: "Question Answering", url:"Q&A"}, 
    {name: "Classification", url:"classification"}, 
    {name: "Text Summarization", url:"text_sum"}]
     
    const list = names.map((name) =>
        <ListItem name={name}/>
    )
    return (
        <div className={styles.background}>
            <img src={logo} className={styles.image}/>
            <div>{list}</div>

        </div>
    );
}

const ListItem = (props) => {
    const name = props.name
    return ( 
        <Link style={{ color: 'inherit', textDecoration: 'inherit'}} to = {name.url} >
            <div className={styles.itemlist_bg}>{name.name}</div>
        </Link>
    );
}
 

export default VerticalHeader;