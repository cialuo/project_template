import React from "react";
import { useOdooContext } from './contexts/odoo'
import TreeTable from './TreeTable'
const App = (props) => {    
    const { odoo_params } = useOdooContext()
    const { name } = odoo_params || { name: 'employee_assignments' }
    const [data, setData] = React.useState(null)
    React.useEffect(() => {
      try {
        const ws = new WebSocket("ws://localhost:3000/");
        ws.onmessage = ({data}) => {
          setData(data)
        }
      } catch(err) {
        console.log(err);
      }
    }, [])
    return (
        <div>
          <If condition={name === 'employee_assignments'}>
            <TreeTable {...props} />
          </If>
        </div>
    );
};

export default App;
