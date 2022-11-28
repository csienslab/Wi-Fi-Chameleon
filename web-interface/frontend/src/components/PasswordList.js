import React from 'react';
import { Card, Button } from 'semantic-ui-react';
import { epoch_to_time } from '../util';
import "../styles/phish.css";

export default ({ list, doHide, doDelete }) => {
  const shortan = (text) => text.length > 50?text.substring(0, 50)+"...":text;
  return (
    <div className="phish-container">
      <Card.Group>
        {list.map(victim => (
          <Card key={victim.id}>
            <Card.Content>
              <Card.Header>
                <span className="phish-name">{victim.name.length > 0?victim.name:"<Blank>"}</span>
                <span>;</span>
                <span className="phish-password">{victim.password.length > 0?victim.password:"<Blank>"}</span>
              </Card.Header>
              <Card.Meta>From <i>{victim.ssid}</i>, {epoch_to_time(victim.time*1000)}</Card.Meta>
              <Card.Description>
                {shortan(victim.host)}
              </Card.Description>
            </Card.Content>
            <Card.Content extra>
              <div className='ui two buttons'>
                <Button basic color='blue' onClick={() => doHide(victim.id)}>
                  Hide
                </Button>
                <Button basic color='red' onClick={() => doDelete(victim.id)}>
                  Delete
                </Button>
              </div>
            </Card.Content>
          </Card>
        ))}
      </Card.Group>
    </div >
  )
}