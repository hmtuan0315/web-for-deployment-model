import React from 'react';
import styles from './sent_analysist.module.css'
import Dropdown from '../../Components/Dropdown';
import TextArea from '../../Components/TextArea';
import { useState } from 'react';

const SentimentAnalysist = () => {
    const model = [{name:"LSTM", value:"lstm"},
    {name:"BERT", value:"bert"}]
    const examples = [{name:"Tweet dataset", value:"tweet"}]
    const [type, setType] = useState("")
    const [dataset, setDataset] = useState("")
    const [exampleText, setExampleText] = useState("")
    
    const handleChangeType = (event) => {
        setType(event.target.value);
    };
    const handleChangeDataset = (event) => {
        setDataset(event.target.value)
        if(event.target.value == "tweet"){
            setExampleText("Too bad, I will not be around. I lost my job and can not even pay my phone bill lmao aw shuck")
        } else {
            setExampleText("")
        }
    }

    const handleChange = (event) => {
        setExampleText(event.target.value)
    }

    const handleClick = (event) => {
        const axios = require('axios')
        axios.post('http://127.0.0.1:5000/cls_lstm', {
            text: "it's a bad movie out of the time"
        },{
            'Content-Type': 'application/json',
            withCredentials: true,
        })
        .then(function (response) {
            // handle success
            console.log(response.data);
            
        })
    }
    
    return ( 
        <div className={styles.background}>
            <div>Sentiment Analysist</div>
            <div>Modern NLP models can assign a category to a text and classify it</div>
            <div>Try it yourself!</div>
            <div style={{display:'flex', alignItems: "center"}}>
                <div>Let's use the</div>
                <Dropdown list={model} type={type} handleChange={handleChangeType}/>
                <div>model</div>
            </div>
            <div style={{display:'flex', alignItems: "center"}}>
                <div>Now enter your text or use our examples</div>
                <Dropdown list={examples} type={dataset} handleChange={handleChangeDataset}/>
            </div>
            <TextArea exampleText={exampleText} handleChange={handleChange}
                handleClick={handleClick}
            />
        </div>
     );
}
 
export default SentimentAnalysist;
