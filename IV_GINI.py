def func_IV_GINI_KS(table,var,target): ### Функция подсчёта IV GINI KS
## Version1
    pt=pd.pivot_table(table,index=[var],values=[target], aggfunc={target:[np.size, np.mean, np.sum]})

    pt_s1=pd.DataFrame({var:pt.index.tolist(),'T':pt[target]['size'],'Events':pt[target]['sum'],

                       'E_rate%':np.round(100*pt[target]['mean'],1)},index=None)

    pt_s2=pd.DataFrame({'T':pt_s1['T'],'Events':pt_s1['Events'],'E_rate%':pt_s1['E_rate%']})

    pt_s=pt_s2.reset_index() ###Чтобы удалить индексы     

 

    ##Создаём вспомогательные переменные

    pt_s['T%']=np.round(100*pt_s['T']/pt_s['T'].sum(),1)

    pt_s['E%']=np.round(100*pt_s['Events']/pt_s['Events'].sum(),1)

    pt_s['Non_Events']=pt_s['T']-pt_s['Events']

    pt_s['NE%']=np.round(100*pt_s['Non_Events']/pt_s['Non_Events'].sum(),1)

    pt_s['WoE']=round(np.log(pt_s['NE%']/pt_s['E%']),1)

    pt_s['Odds']=np.round(pt_s['Non_Events']/pt_s['Events'],1)

    pt_s['T%_cum']=pt_s['T%'].cumsum()

    pt_s['E%_cum']=pt_s['E%'].cumsum()

    pt_s['E%_cum1']=pt_s['E%'].cumsum()

    pt_s['NE%_cum']=pt_s['NE%'].cumsum()

    pt_s['Lift']=round(pt_s['E_rate%']/(100*pt_s['Events'].sum()/pt_s['T'].sum()),1)

    pt_s['IV_interm']=( (pt_s['Non_Events']/pt_s['Non_Events'].sum()-pt_s['Events']/pt_s['Events'].sum())*

                         np.log((pt_s['Non_Events']/pt_s['Non_Events'].sum())/(pt_s['Events']/pt_s['Events'].sum())) )

    pt_s['E%_cum_lag']=pt_s['E%_cum'].shift(1)

    pt_s['NE%_cum_mult']=np.where(np.isnan(pt_s['NE%_cum'].shift(1))==True,pt_s['NE%_cum'],

                                  pt_s['NE%_cum'].shift(1)+pt_s['NE%_cum'])

    pt_s_last=pt_s[[var,'T','T%','Non_Events','NE%','Events','E%','E_rate%','WoE','Odds','Lift','T%_cum','E%_cum','NE%_cum','E%_cum1']]

    #pt_s_last

    #pt_s

 

    ## Создаём агрегатную таблицу

    pt_s_agg1=pd.DataFrame({var:['z1)TOTALS'],'T':pt_s_last['T'].sum(),'T%':['100'],

                            'Non_Events':pt_s_last['Non_Events'].sum(),'NE%':['100'],

                            'Events':pt_s['Events'].sum(),

                            'E%':['100'],'E_rate%':round(100*pt_s['Events'].sum()/pt_s['T'].sum(),1),

                            'WoE':['IV='],'Odds':round(np.ma.masked_invalid(pt_s['IV_interm']).sum(),3), ##Чтобы игнорить inf

                            'Lift':['GINI%='],

                            'T%_cum': round(100*( 1- (pt_s['NE%_cum_mult']*pt_s['E%']).sum()/10000),2), ##GINI

                            'E%_cum':['KS%='],

                            'NE%_cum':np.abs(pt_s['E%_cum']-pt_s['NE%_cum']).max(),##KS

                            'E%_cum1':['.']})

    pt_s_agg1=pt_s_agg1[[var,'T','T%','Non_Events','NE%','Events','E%','E_rate%','WoE','Odds','Lift','T%_cum',

                         'E%_cum','NE%_cum','E%_cum1']]

    #pt_s_agg1

 

 

    df_iv_gini_ks=pd.concat([pt_s_last, pt_s_agg1])

   

    return df_iv_gini_ks

## Применять так: func_IV_GINI_KS(table=df_train,var='Merger',target='Grace_flag')