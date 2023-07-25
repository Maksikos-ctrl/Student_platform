import conf

from typing import Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging




##############################################
# BLOCK FOR COMMON INTERACTION WITH DATABASE #
##############################################


engine = create_async_engine(conf.REAL_DATABASE_URL, future=True, echo=True)


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""

    try:
        # gets asynchronous object from database
        session: AsyncSession = async_session()
        logging.info("Acquiring database session...")
        yield session

    except Exception as e:
        logging.error(f"Exception occurred while acquiring database session: {e}")
        raise

    finally:
        await session.close()
        logging.info("Database session closed.")