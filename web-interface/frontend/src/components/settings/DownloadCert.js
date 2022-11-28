import React from 'react';
import { Segment, Header, Button } from 'semantic-ui-react';
import { Link } from 'react-router-dom';

export default () => (
    <Segment>
        <Header as='h2'>Self-Signed Certificate</Header>
        <span style={{marginRight: "1em"}}>Download Wi-Fi Chameleon's certificate.</span>
        <Button as={Link} to="/wifi-chameleon.crt" target="_blank" download>Download .crt</Button>
        <Button as={Link} to="/wifi-chameleon.key" target="_blank" download>Download .key</Button>
        <Button as={Link} to="/wifi-chameleon.pem" target="_blank" download>Download .pem</Button>
    </Segment>
)