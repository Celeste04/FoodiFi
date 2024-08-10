import React, {useState} from 'react'
import ListForm from './list-form';
import { FaTrashCan } from "react-icons/fa6";
import './list-styles.css';

function ListItem({items, removeItem, updateItem}) {
    const [edit, setEdit] = useState({
        id: null,
        value: ''
    })
  
    const submitUpdate = value => {
      updateItem(edit.id, value);
      setEdit({
        id: null,
        value:''
      })
      if (edit.id) {
        return <ListForm edit={edit} onSubmit={submitUpdate}></ListForm>
      }
    }

  return items?.map((item, index)=>(
    <div className='item-row' key={index}>
        <div className="item-text" key={item.id}>
            {item.text}
        </div>
        <div className="icons"><FaTrashCan onClick={()=>removeItem(item.id)} className="delete-icon"/></div>
    </div>
  ));
}

export default ListItem;
