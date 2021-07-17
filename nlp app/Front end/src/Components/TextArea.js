import React from "react";
import styles from '../Css/TextArea.module.css'
// import { useState, useEffect } from 'react';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import Icon from '@material-ui/core/Icon';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import { green } from "@material-ui/core/colors";

const useStyles = makeStyles((theme) => ({
    button: {
      margin: theme.spacing(1),
    //   colr: green
    },
  }));

const TextArea = (props) => {
    const exampleText = props.exampleText
    const classes = useStyles();
    const handleClick = props.handleClick
    const handleChange = props.handleChange
    return ( 
        <div className={styles.background}>
            <div className={styles.passage_title}>Text</div>
            <textarea placeholder="Paste your text here" onChange={handleChange}
                    className={styles.text_area} value={exampleText}
                    rows="10" cols="50">
            </textarea>
            <div style={{textAlign:"right"}}>
                <Button
                    style={{backgroundColor:"#6ca858", color:"white", height:"40px", fontSize:"16px"}}
                    onClick={handleClick}
                    variant="contained"
                    // color=green
                    className={classes.button}
                    endIcon={<CloudUploadIcon style={{fontSize:"18px"}}/>}
                >
                    Send
                </Button>
            </div>
        </div>
    );
}
 
export default TextArea;