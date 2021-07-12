import VerticalHeader from './Components/VerticalHeader';
import styles from './App.module.css'
import SentimentAnalysist from './Pages/Sentiment Analysist';
import QuesAnswer from './Pages/Q-A';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function App() {
  return (
    <div className={styles.App}>
        <Router>
          <VerticalHeader/>
          <Switch>
            <Route path="/Q&A">
              <QuesAnswer/>
            </Route>
            <Route path="/">
              <SentimentAnalysist/>
            </Route>
        </Switch>
        </Router>
    </div>
  );
}

export default App;
