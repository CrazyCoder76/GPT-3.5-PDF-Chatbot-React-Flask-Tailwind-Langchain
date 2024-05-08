import { useEffect, useState } from 'react'
import ChatComponent from '../../components/chatComponent'
import Leftsidebar from '../../components/leftSideBar'
import { useToast } from '../../components/toast'
import 'react-responsive-modal/styles.css';
import { Modal } from 'react-responsive-modal';
import apiClient from '../../utils/apiClient'
import ChatbotInterface from '../../components/chatbotInterface'
import ChatbotModel from '../../components/chatbotModel'

const Dashboard = () => {
    const { addToast } = useToast();
    const [session_id, setSessionId] = useState<string>();
    const [bot_id, setBotId] = useState<string>('');
    const [mode, setMode] = useState<number>(0);
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    const onSelectChatbot = (id: string) => {
        apiClient.post(`${import.meta.env.VITE_API_URL}/chatbot/create_session`, {
            chatbot_id: id
        })
            .then(response => {
                setMode(0)
                setSessionId(response.data)
            })
            .catch(reason => {
                addToast(reason.response.data.message, 'error')
            })
    }

    const deleteBotClicked = async () => {
        
        const res = await apiClient.post(`${import.meta.env.VITE_API_URL}/chatbot/delete_chatbot`, {
            id: bot_id
        });
        
        if(res.status != 200) {
            addToast(res.data.message, 'error');
        }

        setBotId("");
        setIsModalOpen(false);
    }

    const onChatbotInterface = (id: string) => {
        setMode(1);
        setBotId(id);
    }

    const onChatbotModel = (id: string) => {
        setMode(2);
        setBotId(id);
    }

    const onChatbotDelete = async (id: string) => {
        setIsModalOpen(true);
        setBotId(id);
    }

    useEffect(() => {
    }, [bot_id]);

    return (
        <>
            <div className="flex h-[100vh]">
                
                <Leftsidebar
                    onSelectChatbot={onSelectChatbot}
                    onChatbotInterface={onChatbotInterface}
                    onChatbotDelete={onChatbotDelete}
                    onChatbotModel={onChatbotModel}
                />
                {
                    mode == 0 && session_id &&
                    <ChatComponent session_id={session_id} />
                }
                {
                    mode == 1 && bot_id &&
                    <ChatbotInterface bot_id={bot_id} />
                }
                {
                    mode == 2 && bot_id &&
                    <ChatbotModel bot_id={bot_id} />
                }
                {
                    isModalOpen && bot_id &&
                    
                    <Modal
                        open={isModalOpen}
                        onClose={() => { setIsModalOpen(false); }}
                        classNames={{ modal: "customModal" }}
                        center
                    >
                        <h2 className='text-2xl'>Confirm chatbot deletion</h2>
                        <p className='mb-5 mt-2'>Are you sure you want to delete this chatbot?<br></br>This action cannot be undone.<br></br>Deleting the chatbot will permanently remove it from your account. Any associated data or configurations will also be lost.</p>
                        <div className=' flex justify-end items-center gap-4'>
                            <button className='btn btn-error' onClick={deleteBotClicked}>Delete</button>
                            <button className='btn' onClick={() => { setIsModalOpen(false); }}>Cancel</button>
                        </div>
                    </Modal>
                }
            </div>
        </>
    )
}

export default Dashboard