package com.jobsmatcher.company.dao.impl;



import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;
 















import org.apache.log4j.Logger;
import org.hibernate.Query; 
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.jobsmatcher.company.dao.PositionDao;  
import com.jobsmatcher.company.model.Position; 
import com.jobsmatcher.company.model.PositionPostDate;
import com.jobsmatcher.company.model.ViewPositionPostDate;



@Repository
public  class PositionDaoImpl extends AbstractDaoImpl<Position, String> implements
		PositionDao {

	
	
	final static Logger logger = Logger.getLogger(PositionDaoImpl.class); 
	protected PositionDaoImpl() {
		
        super(Position.class);
        
        
    }
	
	protected PositionDaoImpl(Class<Position> entityClass) {
		super(entityClass);
		// TODO Auto-generated constructor stub
	}

	@SuppressWarnings("unchecked")
	@Transactional(readOnly=true)
	@Override
	public List<Position> findAll() {
		return (List<Position>) getCurrentSession().createQuery("from Position").list(); 
	}

	@Override
	public Position findByName(String name) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	@Transactional(readOnly=true)
	@SuppressWarnings("unchecked")
	public List<Position> getPositionByCompany(String id,int start,int limit, int page) {
		List<Position> users = new ArrayList<Position>();
		//System.out.println("company id :" + id); 
		
		String sql = "from Position p where p.id_company = " + id;
		Query query = getCurrentSession().createQuery(sql).setFirstResult(start);
		
		if (limit >0){
			query = query.setMaxResults(limit);
		}
		
			//.setParameter(0, id)
		users = query.list();
 	
		 return users;
	}

	@Override
	public void deleteById(Position id) {
		StringBuffer sb = new StringBuffer();
		sb.append("delete from job_position where id_position = ").append(id.getId_position());
		
		int v = getCurrentSession().createSQLQuery(sb.toString()).executeUpdate(); 
		//System.out.println(v); 
		 
		logger.info("Delete Positon : " + v);
	}

	@Override
	@Transactional
	public boolean updatePosition(Position position) {
		//System.out.println("update company");
		
		try{
			DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
		   
			
			StringBuffer sb = new StringBuffer();
			
			sb.append("update job_position set ");
			sb.append("position = '" ).append( position.getPosition()  ).append( "'"  ).append( " , ");
			sb.append("basic_qualification = '"  ).append( position.getBasic_qualification() ).append( "'").append( " , ");
			sb.append("position_no = '"  ).append( position.getPosition_no() ).append( "'").append( " , ");
			sb.append("source = '"  ).append( position.getSource() ).append( "'").append( " , ");
			sb.append("personal_characters = '"  ).append( position.getPersonal_characters() ).append( "'").append( " , ");
			sb.append("job_popose = '"  ).append( position.getJob_popose()   ).append( "'").append( " , ");
			sb.append("job_description = '"  ).append( position.getJob_description()).append( "'").append( " , ");
			sb.append("experience = '"  ).append( position.getExperience()  ).append( "'").append( " , ");
			sb.append("post_date = '"  ).append( df.format(position.getPost_date())       ).append( "'");
			
			sb.append(" where id_position = '" + position.getId_position() + "'");
 
			
			 
			
			 
			
			System.out.println("saveOrUpdate");
			int v = getCurrentSession().createSQLQuery(sb.toString()).executeUpdate(); 
			 //System.out.println(v);
			//getCurrentSession().update(newCom);
			 
			//System.out.println(serial);
			 sb = null;
			 df = null;
			return true;
		}
		catch(Exception ex){
			ex.printStackTrace();
			return false;
		}
		  
		
	}

	 

	@Override
	public void deleteByCompany(int id) {
		StringBuffer sb = new StringBuffer();
		sb.append("delete from job_position where id_company_data = ").append(id );
		
		int v = getCurrentSession().createSQLQuery(sb.toString()).executeUpdate(); 
		
		logger.info("Delete job_position : " + v);
	}

	@Override
	public int getSizePositionByCompany(String id) {
		String sql = "select count(*) from Position where id_company_data = " + id;
		int count = ((Long)getCurrentSession().createQuery(sql).uniqueResult()).intValue();
		return count;
	}

	@SuppressWarnings("unchecked")
	@Override
	public List<ViewPositionPostDate> getPositionPostDateById(int id,int start,int limit, int page) {
		 
		String sql = "from Position where id_position = " + id;
		 sql = "from Position p inner join p.PositionPostDates where p.id_position = " + id;
		
		Query query = getCurrentSession().createQuery(sql).setFirstResult(start);
		
		if (limit >0){
			query = query.setMaxResults(limit);
		}
		
		List<Object[]> listResult  = query.list();
		List<ViewPositionPostDate> listPostDate = new ArrayList<ViewPositionPostDate>();
		
		
		for (Object[] aRow : listResult) {
			Position position = (Position) aRow[0];
			PositionPostDate positionPostDate = (PositionPostDate) aRow[1];
			
			ViewPositionPostDate viewPositionPostDate = new ViewPositionPostDate();
			viewPositionPostDate.setPosition(position.getPosition());
			viewPositionPostDate.setId_position_post_date(positionPostDate.getId_position_post_date());
			viewPositionPostDate.setPost_date(positionPostDate.getPost_date());
			
			listPostDate.add(viewPositionPostDate); 
		}
		
		  
		
		
		return listPostDate;
	}

	@Override
	public int getSizePositionPostDateById(int id) {
		String sql = "select count(*) from PositionPostDate ppd inner join Position p   where p.id_position = " + id;
		sql = "select count(*) from Position p inner join p.PositionPostDates where p.id_position = " + id;
		int count = ((Long)getCurrentSession().createQuery(sql).uniqueResult()).intValue();
		
		logger.info("count PositionPostDate : " + count); 
		
		return count;
	}
	
	

}
