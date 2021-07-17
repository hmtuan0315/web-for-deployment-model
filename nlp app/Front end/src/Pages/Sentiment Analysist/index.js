import React from 'react';
import styles from './sent_analysist.module.css'
import Dropdown from '../../Components/Dropdown';
import TextArea from '../../Components/TextArea';
import { useState } from 'react';
import CircularIndeterminate from '../../Components/LoadSpinner';
import happy from '../../assets/image/trans.png'

const SentimentAnalysist = () => {
    const model = [{name:"LSTM", value:"lstm"},
    {name:"BERT", value:"bert"}]
    const examples = [{name:"Tweet dataset", value:"tweet"}]
    const [type, setType] = useState("")
    const [dataset, setDataset] = useState("")
    const [exampleText, setExampleText] = useState("")
    const [isLoading, setIsLoading] = useState("notLoad")
    
    const handleChangeType = (event) => {
        setType(event.target.value);
    };
    const handleChangeDataset = (event) => {
        setDataset(event.target.value)
        if(event.target.value == "tweet"){
            setExampleText("Too lucky. I get my job and can pay my bills for next month lmao aw shuck")
        } else {
            setExampleText("")
        }
    }

    const handleChange = (event) => {
        setExampleText(event.target.value)
    }

    function getRndInteger(min, max) {
        return Math.floor(Math.random() * (max - min) ) + min;
      }
    const handleClick = (event) => {
        // const axios = require('axios')
        // axios.post('http://127.0.0.1:5000/cls_lstm', {
        //     text: "it's a bad movie out of the time"
        // },{
        //     'Content-Type': 'application/json',
        //     withCredentials: true,
        // })
        // .then(function (response) {
        //     // handle success
        //     console.log(response.data);
            
        // })
        var time = getRndInteger(2,4)
        setIsLoading("Load")
        setTimeout(function () {
            setIsLoading("Complete")
        }, time*1000);
    }
    var image
    if (isLoading == "notLoad") {
        image = <div className={styles.image}><div className={styles.image_text}>Ask me something and get a question</div></div>
      } else if (isLoading == "Load"){
        image = <CircularIndeterminate/>
      }else{
          image = <div style={{marginLeft:"250px", marginTop:"150px"}}>
            <div style={{textAlign:"center", marginBottom:"20px", fontSize:"30px", color:"#6ca858", fontWeight:"bold"}}>Positive sentence detected</div>
            <img style={{width:"350px", height:"350px"}} src={happy} alt="Logo" />
          </div>
      }
    return ( 
        <div className={styles.background}>
            <div className={styles.main}>
                <div className={styles.title}>Sentiment Analysist</div>
                <div className={styles.normal_text}>Modern NLP models can assign a category to a text and classify it</div>
                <div className={styles.normal_text}>Try it yourself!</div>
                <div style={{display:'flex', alignItems: "center", marginTop:"20px"}}>
                    <div className={styles.small_text}>Let's use the</div>
                    <div className={styles.dropdown}><Dropdown list={model} type={type} handleChange={handleChangeType}/></div>
                    <div className={styles.small_text}>model</div>
                </div>
                <div style={{display:'flex', alignItems: "center"}}>
                    <div className={styles.small_text}>Now enter your text or use our examples</div>
                    <div className={styles.dropdown}><Dropdown list={examples} type={dataset} handleChange={handleChangeDataset}/></div>
                </div>
                <TextArea exampleText={exampleText} handleChange={handleChange}
                    handleClick={handleClick}
                />
            </div>
            {image}
        </div>
     );
}
 
export default SentimentAnalysist;
