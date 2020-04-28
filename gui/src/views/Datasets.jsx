import React, { Component } from 'react'
import {
    Card,
    CardHeader,
    CardBody,
    CardFooter,
    CardTitle,
    Row,
    Col,
    Button
  } from "reactstrap";


export class Datasets extends Component {
    render() {
        return (
            <div className="content">
                <Row>
                    <Col lg="3" md="3" sm="3">
                        <div onClick={() => alert("ye")}>
                        <Card className="card-button add">
                        <CardBody>
                        <Row>
                            <Col md="4" xs="5">
                            <div className="icon-big text-center">
                                <i className="nc-icon nc-simple-add" />
                            </div>
                            </Col>
                            <Col md="8" xs="7">
                            <div className="numbers">
                                <CardTitle tag="p">Add</CardTitle> 
                            </div>
                            </Col>
                        </Row>
                        </CardBody>
                        <CardFooter>
                        <hr />
                        <div className="stats">
                            <i className="fas fa-info-circle" style={{color:'white'}} /> See accepted format
                        </div>
                        </CardFooter>
                        </Card>
                        </div>
                    </Col>
                    <Col lg="3" md="3" sm="3">
                        <div onClick={() => alert("ye")}>
                        <Card className="card-button add">
                        <CardBody>
                        <Row>
                            <Col md="4" xs="5">
                            <div className="icon-big text-center">
                                <i className="nc-icon nc-refresh-69" />
                            </div>
                            </Col>
                            <Col md="8" xs="7">
                            <div className="numbers">
                                <CardTitle tag="p">Change</CardTitle> 
                            </div>
                            </Col>
                        </Row>
                        </CardBody>
                        <CardFooter>
                        <hr />
                        <div className="stats">
                            <i className="fas fa-info-circle" style={{color:'white'}} /> See accepted format
                        </div>
                        </CardFooter>
                        </Card>
                        </div>
                    </Col>
                    <Col lg="3" md="3" sm="3">
                        <div onClick={() => alert("ye")}>
                        <Card className="card-button add">
                        <CardBody>
                        <Row>
                            <Col md="4" xs="5">
                            <div className="icon-big text-center">
                                <i className="nc-icon nc-simple-remove" />
                            </div>
                            </Col>
                            <Col md="8" xs="7">
                            <div className="numbers">
                                <CardTitle tag="p">Delete</CardTitle> 
                            </div>
                            </Col>
                        </Row>
                        </CardBody>
                        <CardFooter>
                        <hr />
                        <div className="stats">
                            <i className="fas fa-info-circle" style={{color:'white'}} /> See accepted format
                        </div>
                        </CardFooter>
                        </Card>
                        </div>
                    </Col>
                </Row>
            </div>
        )
    }
}

export default Datasets
