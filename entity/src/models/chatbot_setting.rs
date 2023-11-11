use serde::{Deserialize, Serialize};
#[derive(Deserialize, Serialize)]
pub struct ChatbotSetting {
    pub id: String,
    pub chatbot_id: String,
    pub name: String,
    pub value: String,
    pub created_at: Option<chrono::NaiveDateTime>,
    pub updated_at: Option<chrono::NaiveDateTime>,
}
