import React from 'react';
import { Table, Header } from 'semantic-ui-react';
import "../styles/wifi.css";

export default ({ list }) => {
  return (
    <div className='wifi-list-container'>
      <Header className="wifi-list-title" as="h3" textAlign="center">
        Daemons List
      </Header>
      <Table className="wifi-list" unstackable>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell textAlign="center" width="12">Service</Table.HeaderCell>
            <Table.HeaderCell textAlign="center" width="4">Status</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {list.map(daemon => (
            <Table.Row key={daemon['name']}>
              <Table.Cell>
                <Header as="h3" textAlign="center">
                  {daemon['name']}
                </Header>
              </Table.Cell>
              <Table.Cell textAlign="center" style={{color: daemon['status'] === "active"?"green":"red"}}>
                {daemon['status']}
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    </div>
  )
}