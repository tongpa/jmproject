package com.jobsmatcher.company.model;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.CascadeType; 
import javax.persistence.FetchType;

import org.hibernate.annotations.Type;


@Entity
@Table(name = "job_position_post_date" )
public class PositionPostDate  implements Serializable{
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	@Id
	@Column(name = "id_position_post_date", unique = true, nullable = false )	
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private int id_position_post_date;
	
	@Column(name = "id_position")
	private int id_position;
	
	@Column(name = "post_date")
	@Type(type="date")
	private Date post_date;
	
	//@ManyToOne
    //@JoinColumn(name = "id_position")
	@ManyToOne(cascade=CascadeType.ALL, optional=true, fetch=FetchType.EAGER)  
    @JoinColumn(name="id_position", referencedColumnName = "id_position", insertable = false, updatable = false)  
	private Position position;
	
	/*@Column(name = "create_date")
	@Type(type="date")
	private Date create_date;
	
	@Column(name = "update_date")
	@Type(type="date")
	private Date update_date;
*/
	
	@Override
	public String toString() {
		return String.format("Post Date [id_position = %d, postdate = %tF]", id_position, post_date);
	}


	public int getId_position_post_date() {
		return id_position_post_date;
	}


	public void setId_position_post_date(int id_position_post_date) {
		this.id_position_post_date = id_position_post_date;
	}


	public int getId_position() {
		return id_position;
	}


	public void setId_position(int id_position) {
		this.id_position = id_position;
	}


	public Date getPost_date() {
		return post_date;
	}


	public void setPost_date(Date post_date) {
		this.post_date = post_date;
	}


	public Position getPosition() {
		return position;
	}


	public void setPosition(Position position) {
		this.position = position;
	}

/*
	public Date getCreate_date() {
		return create_date;
	}


	public void setCreate_date(Date create_date) {
		this.create_date = create_date;
	}


	public Date getUpdate_date() {
		return update_date;
	}


	public void setUpdate_date(Date update_date) {
		this.update_date = update_date;
	}
	
	 */

	
}
