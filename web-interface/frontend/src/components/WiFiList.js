import React from 'react';
import { Table, Header } from 'semantic-ui-react';

export default ({ list, current = false, onClick=null }) => {
  return (
    <div className='wifi-list-container'>
      <Header className="wifi-list-title" as="h3" textAlign="center">
        {current?"Current AP":"Available APs"}
      </Header>
      <Table className="wifi-list" unstackable selectable>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell textAlign="center" width="12">SSID</Table.HeaderCell>
            <Table.HeaderCell textAlign="center" width="4">Signal Level</Table.HeaderCell>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {list.map(ap => (
            <Table.Row className="clickable" key={ap['bssid']} onClick={onClick===null?undefined:() => {
              const result = window.confirm(current?"Stop attack?":`Attack ${ap['ssid']}?`);
              if(result) onClick(ap['ssid']);
            }}>
              <Table.Cell>
                <Header as="h3" textAlign="center">
                  {ap['ssid']}
                </Header>
              </Table.Cell>
              <Table.Cell textAlign="center">{ap['signal level']}</Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    </div>
  )
}
