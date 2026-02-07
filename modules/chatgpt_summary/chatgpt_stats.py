import pandas as pd

def run_chatgpt_stats():
    df = pd.read_json('./conversations.json')

    all_queries = []
    query_count_list = []
    convo_cat_list = []

    convo_list = df['title'].tolist()
    for convo in convo_list:
        if any(techword in convo for techword in ['Python','GCP','Databricks','VSCode','Excel','SQL','Power BI','Collibra']):
            convo_cat_list.append('Tech Questions')
        elif any(reflect in convo for reflect in ['Reflections', 'Message Crafting', 'Therapy']):
            convo_cat_list.append('Personal Guidance')
        else:
            convo_cat_list.append('General Information')

    for convo in df['mapping']:
        query_count = 0
        for chat_id in (list(convo.keys())):
            for message_id in list(convo[chat_id].keys()):
                if isinstance(convo[chat_id][message_id],dict) and convo[chat_id][message_id]['author']['role']=='user':
                    all_queries.append(convo[chat_id][message_id]['content']['parts'][0])
                    query_count += 1
        query_count_list.append(query_count)

    total_queries = sum(query_count_list)
    query_percent_print_list = [f'{round(100*i/total_queries,1)}%' for i in query_count_list]
    query_percent_list = [round(100*i/total_queries,1) for i in query_count_list]

    query_counts_df = pd.DataFrame(
        {
            'Conversation'              : convo_list,
            'Category'                  : convo_cat_list,
            'Num of Queries'            : query_count_list,
            'Percent of Queries'        : query_percent_list,
            'Percent of Total Queries'  : query_percent_print_list
        }
    )

    category_df = query_counts_df.groupby(['Category']).sum()
    category_df = category_df[['Percent of Queries']].sort_values(by=['Percent of Queries'],ascending=False)
    query_counts_df = query_counts_df[['Conversation','Num of Queries','Percent of Total Queries']].sort_values(by=['Num of Queries'],ascending=False)

    print(query_counts_df)
    print(category_df)
