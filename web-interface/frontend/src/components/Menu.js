import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Icon, Menu } from 'semantic-ui-react';
import useWindowDimensions from '../hooks/dimension';
import '../styles/menu.css';

export default () => {
  const location = useLocation();
  let path = location.pathname;
  if (path[0] === "/") path = path.substring(1);
  const width = useWindowDimensions().width;
  const phone = width < 500;
  const items = [
    // path, icon, content
    ["wifi", "wifi", "Wi-Fi"],
    ["phishing", "user secret", "Phishing"],
    ["settings", "settings", "Settings"],
    ["tests", "flask", "Tests"],
  ]

  return (
    <div id="menu-div">
      <Menu icon='labeled' vertical={!phone} widths={phone?items.length:undefined}>
        {items.map(item => (
          <Menu.Item
            key={item[0]}
            name={item[0]}
            active={path === item[0]}
            to={item[0]}
            as={Link}
          >
            <Icon name={item[1]} />
            {item[2]}
          </Menu.Item>
        ))}
      </Menu>
    </div>
  )
}