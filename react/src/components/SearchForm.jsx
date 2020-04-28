import React from "react";
import TopNavBar from "./TopNavBar"
import SimpleTweetCard from "./SimpleTweetCard"
import '../CSS/App.css';
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'

export default class SearchForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = { value: '', tweetIds: [] };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({ value: event.target.value });
    }

    createTwitterCard(tweetId){
        console.log(tweetId)
        return(
            <SimpleTweetCard
                key={tweetId}
                tweetId={tweetId}
             />
        );
    }

    handleSubmit(event) {
        var query = this.state.value
        event.preventDefault();
        fetch('https://backend-dot-bigdata-covid.uc.r.appspot.com/Search/' + query).then(res => res.json()).then(data => {
            this.setState({
                tweetIds: data
            })
        })
    }

    render() {
        return (
            <div className="App">
                <TopNavBar />
                <Form className="searchinput" onSubmit={this.handleSubmit}>
                    <Form.Group controlId="formBasicEmail">
                        <Form.Label className="searchLabel">Enter term to seach Twitter for COVID-19 related Tweets</Form.Label>
                        <Form.Control type="input" placeholder="Enter search term" value={this.state.value} onChange={this.handleChange} />
                        <Form.Text className="text-muted">
                        </Form.Text>
                    </Form.Group>

                    <Button variant="primary" type="submit" value="Submit">
                        Submit
            </Button>
                <h3>Results:</h3>
                </Form >
                <dl className="dictionary">{this.state.tweetIds.map(this.createTwitterCard)}</dl>
            </div>
        );
    }
}
